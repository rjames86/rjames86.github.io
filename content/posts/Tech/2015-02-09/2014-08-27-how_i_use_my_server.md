Title:  How I use my Mac Mini Server on Macminicolo
Date: 2015-02-09 22:04
Category: Tech
Tags: Dropbox, efficiency, hazel, scripting
Author: Ryan M

I frequently get asked why I use [Macminicolo][Macminicolo] and if it's worth it. It's a relatively expensive hobby, but it gives me so much benefit that at this point I couldn't live without it. Having an always-on Mac opens up a lot of opportunity and I'm always finding new things to use it for. 
<!-- PELICAN_END_SUMMARY -->  

If you haven't already read it, Macminicolo has already posted their own [50 ways to use your server][50ways]. I thought it would be worth sharing some of the ways that I use my Mac Mini. Some of these things I've already shared in the past and I'll be sure to post more details on any of the other things in the future. 

[50ways]: http://blog.macminicolo.net/post/47038825502/50-ways-to-use-your-server
----

[TOC]

## Syncing and Backup ##


**Dropbox**

All of my Dropbox files are synced to this computer. My MacBook Air doesn't have enough space to store all my files and so the Mac Mini is the place where I store all my Dropbox files locally so that I can run workflows and have a local backup. 

**Off-site Backup**

Since I have so much space, I use it as an offsite backup for my laptop using Arq over sftp. Nothing too fancy or special here, but it's a nice alternative to Time Machine as an offsite backup. 

## Hazel

[Hazel][Hazel] may be my favorite reason for having an always-on Mac. Hazel watches multiple folders in my Dropbox folder and keeps my Dropbox much more organized than I ever would manually. Some of my favorites are

**Organizing my photos**

I've talked about this one a bit in the past. I love that Carousel will automatically upload my photos to Dropbox, but the Camera Uploads folder becomes a wasteland of files if you don't organize them on a regular basis. I move all of my photos into a photos folder organized by year. I've written about this in more detail [here][organize photos]. If you use Carousel and have ever saved photos that someone else shared with you, you'll know that a completely different folder is created in Dropbox called Carousel. In this folder, more folders are created with the email address of the person who shared the photos with you. I want these photos in my normal photos folder and so I run the same set of rules as my Camera Uploads to reorganize these photos. The only exception is that I add a "carousel" tag to these photos so that I know they were added from Carousel. 

![organize_photos]({static}organize_photos.png)

I take a selfie every day (620 days and counting) and am far too lazy to move that photo to its own special photo every day. I've made sure to always use Camera+ to take these photos. Hazel looks at the metadata of the photos in Camera Uploads and if the photo was taken by the front camera and the app used to create the file was Camera+, it's moved to its own special folder and renamed to just YYYY-MM-DD. 

**Publishing my blog**

I use a static blog generator, [Pelican][pelican],  which means that I can store the entire project, including the Python code in my Dropbox account. While I'm on my Mac, it's easy to run a shell script to publish my blog. On iOS, it's not quite as easy and so I use Hazel to watch my blog folder for a file called 'publish.blog'. If that file exists, the shell script is run and the file is then deleted. Since my girlfriend runs her blog over at [keepitlit.co](http://www.keepitlit.co) with the same static blog generator, it's much simpler for her to create a file just like this when she wants to publish her blog. 

**IFTTT → Dropbox → Flickr → AppleTV**

I have a rule set up in IFTTT that will append to a text file each time my girlfriend or I post a photo to Instagram. Each time this file runs, I have a script that uploads the photo to a private Flickr album. My AppleTV is then set to that album so that we have an updated list of photos as a screen saver. I realize I could do this directly in IFTTT, but I don't like that you can't make the album private. 

Download the script [here]({static}ifttt_to_flickr.py)

**Time sensitive Dropbox shared links**

If you have a Dropbox Pro account,  this is now a feature built right in.  I have two folders named "One day" and "One week". Files that I want to share temporarily are copied to that folder. After the set amount of time, the files will be deleted and I'm sent a push notification. For the one week folder, I also get a notification the day before to remind me that it'll get deleted.

You can download the 1 Day rule [here]({static}1 day.hazelrules). Be sure to add your own Pushover key and secret, or remove it if you don't need notifications.

![1%20day]({static}1%20day.png)

**Scanned files**

This folder is for files added from my Fujitsu ScanSnap or Scanbot for iOS. If the file hasn't been OCR'd already, a script will run to launch PDFPenPro and OCR the file. I then have a series of rules set up to move the files based on their names.

Work Receipts is my favorite. When I scan a receipt in Scanbot, I have a snippet "wwr" that expands to "Work receipt". Hazel watches for any new PDFs with that string in the filename. Files are then moved to my expenses folder, organized by date. It then creates a new task in Due.app with a due date of one week in the future so that I'll remember to do my expenses for the file. I no longer have to keep all my receipts and I'll never forget to actually do the expenses[^1].

Business cards obviously moves any business cards to a special folder. Hazel watches for a string match in the filename to know to file these as well. Finally, personal receipts moves the files to my own receipts folder for archiving.

## Web Server

I use this Mac Mini as a web server since it has more than enough bandwidth and speed. I had never set up an server before, and so this was a fun learning experience to do it all myself. I run a very basic Apache, MySQL, PHP stack for my web server. 

### Blogs

I host this blog from my Mac Mini as well as a couple of others, most notably my girlfriend's. 

### Site Analytics

I don't want to use Google Analytics. They know enough about me already and so I use an open source version called Piwik. I've been fairly happy with it so far. 

### URL Shortening

I don't like long urls and will shorten them whenever I can. When I publish my blog, I always shorten the URL. I like having full control over that and so I'm using [yourls][yourls] to shorten and track URLs. 

### VPN ###

I was running OS X Server and used the Mac Mini as a VPN server. Since upgrading to Yosemite, I haven't gotten around to upgrading server, but it's on the todo list. Check out Macminicolo's blog for some great instructions on setting up a VPN [here][VPN].

### Tapiriik ###

When I'm out cycling, I use a Garmin GPS. Most of my friends use RunKeeper, and I prefer Strava over all of the services. [Tapiriik][Tapiriik] is a great service that lets you keep your fitness services all in sync, including syncing TCX files to your Dropbox account. It's open source, so you can run a local version on your own computer.

### WebDAV

When I was using Omnifocus, I didn't want to sync my database through their servers. I could be wrong, but I don't believe it's encrypted on their servers. I feel much better knowing that it's on my machine and I have completely control of it. I have set up my own WebDAV server so that I can sync my database. It's been extremely fast and reliable. 

## Automation and Scripts

I have crons running on an hourly, daily and weekly bases. I don't want to bore you with all of them, but here are a few of the better ones. 

**getmail**

I use getmail  for archiving my Gmail daily (they've been known to lose data once in a while). I've never needed to use it, but if I ever decide to change providers or Gmail just hits the delete key someday, I'll have a complete backup of my email. A great introduction to getmail can be found [here][getmail]

**Slogger**

I love Slogger and Day One. I've customized a lot of the current plugins and even wrote my own for Instagram. You can read more about it [here][slogger instagram]

**Download Pinboard**

My updated version of Brett Terpstra's pinboard → webloc file script to have tagged webloc files locally. You can read more about this project [here][pinboard]. 

**Face detection → Finder tags**

I don't want to use iPhoto, Aperture or Picasa as a photo management application. Instead, I use Picasa to harvest the facial recognition data, and then have a script that applies Finder tags of the person's name to the photo. I haven't shared this one, because it's not done yet, but it's functional. It's a lot of fun to be able to get all the photos of a person with a simple Spotlight search. Hopefully I can share this in the near future.

**Dropbox Deletions**

I like to keep tabs on my shared folders and any scripts that might be running in my Dropbox account. I parse my Dropbox RSS feeds for deletions of more than 50 files and send myself a push notification with Pushover.

You can download the script [here][dropbox events]

**Dropbox inbox**

Throughout the week, I'll add files to an "Inbox" in my Dropbox folder. On the weekends, I send myself a push notification if there have been any files added so that I can deal with them.

## Media

I don't have a lot of media. I've never been attached to the idea of owning my music or video and stream whatever I can. For any content that I've ripped over the years, I have [Plex][plex] running on my Mac Mini. Again, since the connection is so fast, there's little to no lag when streaming something from home or on my phone. 



[^1]: I've recently switched from Omnifocus to Due2. It took me a bit to figure out how to programmatically create task items, especially if I want emojis in it. See [this][Emojis] post for a good reason to use emojis for tasks in Due. If you're interested, [here][dueapp] is the script I wrote to create tasks in Due for Mac within Hazel.

[getmail]: http://www.makethenmakeinstall.com/2013/02/script-gmail-backup-with-getmail-on-linux/
[slogger instagram]: http://ryanmo.co/2014/09/04/instagram-slogger/
[pinboard]: {static}../2014-12-23/2014-12-23_Download-Pinboard-as-Webloc-Files.md
[organize photos]: http://ryanmo.co/2014/01/11/my-photo-workflow/
[pelican]: http://blog.getpelican.com
[Hazel]: http://www.noodlesoft.com/hazel.php
[Emojis]: http://unduressing.com/post/108269360039/how-i-use-due-2-come-with-me-if-you-want-to-live
[dueapp]: {static}due_hazel.scpt
[yourls]: http://yourls.org
[dropbox events]: {static}dropbox_events.py
[plex]: https://plex.tv
[Macminicolo]: http://www.macminicolo.net
[VPN]: http://blog.macminicolo.net/post/102283942903/setup-a-vpn-with-yosemite-server-10-10
[Tapiriik]: https://tapiriik.com
