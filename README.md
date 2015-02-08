ia-ul-from-youtubedl
================

Uploads all videos in current directory with metadata you downloaded using youtube-dl

**Written in python with the internetarchive module)**

Using internetarchive module version 0.7.9
Using python version 2.6
Using youtube-dl version 2015.01.25

Visit https://pypi.python.org/pypi/internetarchive for more information on the internet archive module

Visit http://rg3.github.io/youtube-dl/ for more information on youtube-dl

## Before You Run

Download the internetarchive module

	sudo pip install --upgrade internetarchive

Download youtube-dl
	
	sudo pip install --upgrade youtube_dl

In the directory of your choosing, download one or more videos with youtube-dl using --write-info-json

	/youtube-dl -c --write-info-json YOUR_VIDEO_URL_HERE

Now after this runs, drop the ia-ul-from-youtubedl script into the current directory.
**Edit the script to use your secret and access keys from internet archive:** https://archive.org/account/s3.php
**Edit the metadata subject tags, or comment out the whole line to not use**

## Quickstart Example

Find a video or playlist of videos you want to download and upload to the internet archive

	 https://www.youtube.com/playlist?list=PLI6R9qwXheraD43gyVcPCwRI8F4NyKZ7F

Download with youtube-dl

	/youtube-dl -c --write-info-json https://www.youtube.com/playlist?list=PLI6R9qwXheraD43gyVcPCwRI8F4NyKZ7F

Retrive the ia-ul-from-youtubedl.py script and place it in the directory
Edit the *secret_key*, *access_key*, and *metadata["subject"]* in ia-ul-from-youtubedl.py

Run the script

	python ia-ul-from-youtube-dl.py

Your items will upload to the internet archive.
