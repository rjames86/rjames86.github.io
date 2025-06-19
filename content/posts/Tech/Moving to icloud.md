Title: Moving My Photos to iCloud
Date: 2017-08-25 07:37
Tags: 
Author: Ryan M
Status: draft

For the last six years, Dropbox has been the source for all of my photos and also my photo viewer. Over the last couple of years, Dropbox has slowly deprecated features to the point where I no longer felt like I could actually see my photos. A month or so ago, I decided it was time to find a better solution. 

A few years ago, Dropbox made it really easy to upload, view and share photos. Since then, we've seen the death of Carousel and most recently the deprecation of photo albums, a crippled web view and the ability to share multiple photos on the web. For a short time, I was still using Dropbox as my source of truth for all my photos and using Google Photos as a viewer. It was fine, but I don't want to give Google my photos and it still left me with a sub-par desktop viewing experience. From all that I've seen lately, iCloud photos is getting better. I've grown to really like Photos on my iPhone. I use the memories feature often after taking trips and as a way to see old photos that I had forgotten about. Last month, I bought the 250GB iCloud plan and decided to give iCloud photos an honest try. 

## Importing to Photos.app

My photo library in Dropbox has always been nicely organized by date thanks to Hazel. I hadn't spent any time creating albums within folders. The import into Photos was as easy as selecting my entire photos folder within Dropbox. I was initially worried that Photos.app wouldn't traverse the folder structure to grab all of the media files, but it very slowly found them all and started the import. There wasn't any progress indicator letting me know it was still searching for photos, and I wasted a bunch of time quitting and restarting the app thinking it had stalled. If you do this with a large folder, just let it sit for an hour or so. I kept an eye on the "X photos to import" within photos and compared that to the number of files in my pictures folder to have a rough idea of whether it's file scan had finished. 

	find ~/Dropbox/Pictures -type f | wc -l

## Uploading

This took almost a month. It probably would have been faster, but there were a few reasons that it took so long. The first is my Comcast upload speeds are pathetic. The second is that while it was uploading, our internet connection was crippled to the point that it was unusable. That meant that I would pause the upload while we were home and resume at night and while we were at work. I played around with some UI scripting to quickly pause and resume iCloud syncing[^1]. 

One minor annoyance was that Photos on the Mac prioritized the upload over downloading any new photos I had taken on my phone. iOS did a great job uploading my photos right after I took them. I was worried something was broken since they weren't showing up on my computer, but once the upload eventually finished, it switched to downloading new content. iOS did the right thing and displayed new photos that had been uploaded from my Mac as well as upload my new photos. I assume this is because my Mac is set to download files locally while my phone optimizes storage. 

## Verdict

So far so good. Photos does a good job with search. I'm not searching for anything obscure enough where it hasn't been able to find what I want (although it's dumb that I have to search 'bicycle' instead of 'bike' since that's the category name). My big worry now is what happens when something bad happens. I have a lot of trust in Dropbox, especially since it has a straight forward way of rolling back files. I had no trust that if iCloud decides to delete all my photos that I can get them back easily. I have redundant backups using Arq and Carbon Copy Cloner to make sure that if this ever happens, I can recover. I'm still using Dropbox's camera upload feature as another backup in case I decide I don't want to keep iCloud photos, but as of right now, I'm happy with it. I feel like I can actually look at my photos, which is the entire point of taking them in the first place. 


[^1]: iCloud photos is the one rare place where you get feedback on the progress of the sync. 