# Internet Archive Uploader for videos downloaded through youtube-dl
# Version 0.1
# By Mike Dank
# Usage: python ia-ul-from-youtubedl.py
# Must be run directly in the directory where the videos are
# This scaffolding should easily be adaptable for custom metadata

import internetarchive as ia
import json
import os
import re
import time

## Set up some colors for our cli output. Should work on *nix/win
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

## Set up some basic variables
timeDelay = 10
workingDirectory = os.getcwd()
previousBase = ""
currentBase = ""
access_key = 'YOUR KEY HERE'
secret_key = 'YOUR KEY HERE'

## Let's get into the main loop over the current directory
print("Using files available in " + workingDirectory)
for file in os.listdir(workingDirectory):
	## Make sure we are using only video files
	if file.endswith(".info.json") and not file == previousBase:
        	print("Working on file...\n" + bcolors.OKBLUE + file + bcolors.ENDC)
		previousBase, currentBase = currentBase, file
		commonFile = file.rsplit( ".", 2 )[ 0 ]
		jsonFile = commonFile  + ".info.json"
		print("Extracting info from...\n" + bcolors.OKBLUE + jsonFile + bcolors.ENDC)
		## Now make sure there is a corresponding JSON file
		if os.path.isfile(jsonFile):
			## Generate an internet archive friendly identifier
			sanitized = re.sub(r'[\W_]+', '', commonFile)
			print("Generating identifier...\n" + bcolors.OKBLUE + sanitized + bcolors.ENDC)
			## Load up our JSON
			jsonData = open(jsonFile)
			data = json.load(jsonData)
			jsonData.close()
			print("Attempting to process JSON...")
			## If we have valid JSON, extract some metadata
			if data:
				metadata = {}
				metadata["title"] = str(data["fulltitle"].encode('ascii', 'ignore'))
				metadata["description"] = str(data["description"].encode('ascii', 'ignore')).replace("\n", "<br>")
				metadata["mediatype"] = "movies"
				metadata["collection"] = "opensource_movies"
				metadata["subject"] = ["YOUR", "TAGS", "HERE"]
				print("JSON parse successful! Checking identifier...")
				## Check to see if our identifier is in use
				item = ia.get_item(sanitized)
				if not item.exists:
					## Identifier not in use, let's upload
					print("Identifier cleared for use!")
					print("[uploading]")
					item = ia.Item(sanitized)
					response = item.upload(file, metadata=metadata, access_key=access_key, secret_key=secret_key)
					print("Server Response: " + str(response))
					## Check the response. An HTTP 200 is OK
					if "200" in str(response):
						print("Success, adding other items associated with "  + sanitized) 
						for otherFile in os.listdir(workingDirectory):
							if otherFile.startswith(commonFile) and not otherFile.endswith(".info.json"):
								print("Adding file: " + str(otherFile))
								response = item.upload(otherFile, access_key=access_key, secret_key=secret_key)
								print("Server Response: " + str(response))
								if "200" in str(response):
									print("Done adding  file: " + str(otherFile) + " to item " + str(sanitized))
								else:
									print(bcolors.FAIL + "[ERROR] Server responded with: " + str(response) + bcolors.ENDC + ". Skipping to next file for item")
						print("Success! Item populating at: " + bcolors.OKGREEN + "https://archive.org/details/" + sanitized + bcolors.ENDC)
                                                print("Moving on to next item in [" + str(timeDelay) +"s]")
					else:
						## Server didn't give us a good status, skip this item
						print(bcolors.FAIL + "[ERROR] Server responded with: " + str(response) + bcolors.ENDC + ". Skipping to next item in [" + str(timeDelay) +"s]")
				else:
					## Identifier in use, skip this item
					print(bcolors.FAIL + "[ERROR] Item identifier in use, skipping to next item in [" + str(timeDelay) +"s]" + bcolors.ENDC)
			else:
				## Couldn't load the JSON, skip this item
				print(bcolors.FAIL + "[ERROR] JSON parse failed! Skipping to next item in [" + str(timeDelay) +"s]" + bcolors.ENDC)

		else:
			## No corresponding JSON file (Did you use '--write-info-json' in your youtube-dl command?)
			 print(bcolors.FAIL + "[ERROR] JSON file does not exist! Skipping to next item in [" + str(timeDelay) +"s]" + bcolors.ENDC)

		## Sleep for a while between items
		time.sleep(timeDelay)

## All done!
print("Finished traversing all files in directory!")
