Title: My Photo Workflow
Date: 2014-01-11
Category: Tech
Tags: hazel, automation, dropbox, ios, photos
Author: Ryan M

After listening to the Mac Power Users [episode][mpu] on photo management and reading the slew of follow up blog posts on other photo management workflows, I thought I would share mine as well.  While my workflow will be fairly similar to [Federico Viticci's][viticci] with a few exceptions, I thought I would share the way that I take, organize, view and share my photos.
<!-- PELICAN_END_SUMMARY -->  

[mpu]: http://www.macpowerusers.com/2014/01/05/mac-power-users-171-photo-management/
[viticci]: http://www.macstories.net/tutorials/my-photo-management-workflow-early-2014/

## Taking Photos

My iPhone is one of the main ways that I take photos. Since it's always in my pocket and takes great quality photos, it's by far the easiest way to take photos no matter where I am.  I've had a lot of fun with the iPhone 5S and the burst and slo-mo modes.

I've never considered myself a photographer. For a long time, I had my mom's hand-me-down Olympus E-500. It was a great camera, but I had no idea how to use it and it was bigger than I preferred. Before moving to Ireland, I decided that I wanted to learn the basics of photography and have a camera that would grow with me as I learned more. The Olympus PEN E-P5 had just started pre-order and I decided that this would be my first "real" camera. I only had a few requirements, and it fortunately satisfied both of them: GPS tagging and small/lightweight. I've now had this the E-P5 for a little over 6 months and couldn't be happier. 

![Olympus PEN E-P5]( {attach}ep5.jpg)

## Importing

I only have one main way to upload my photos - Dropbox Camera Uploads. Whether I use the Dropbox app for iOS or the desktop application, my photos end up in the same place to get processed (more on that later in [Organization](#organization)). 

Any photos that are taken on my iPhone are quickly uploaded via the Dropbox app. When I use my E-P5, I will first turn on the built-in Wifi to sync GPS data from my phone to the camera[^1]. Once that is all taken care of, I plug the camera into my laptop and Dropbox grabs the new photos and imports them.

[^1]: The GPS data is stored on the SD card, but I haven't taken the time to see if I can add this metadata after importing from Dropbox 

## Organization {: id="organization"}

I'm still pretty new to Hazel, but dealing with my photos was the reason I decided to bite the bullet and buy it. My Dropbox Camera Uploads folder was nearing 900 photos and I hadn't taken the time to organize them in over a year. 

Before Camera Uploads, I was suffering through iPhoto. It always bothered me that my photos were obfuscated from view. I always found myself wasting time trying to find the original or using the export option. When Camera Uploads was released, I searched for a way to cleanly export my photos into a Year-Month-Event folder structure. I discovered [this script][exportiphoto] that gave me more than what I wanted and solved my problem perfectly. For anyone who wants to use this, the command I used was

	:::bash
	# -x deconflict export directories of same name
	# -d stop use date prefix in folder name
	# -y add year directory to output
    python exporti_photo.py -x -d -y 

I've been using the Year-Month-Event structure for a few years now and have starting running into a slight annoyance. I find myself constantly flipping between months trying to remember when a certain event happened. I finally came to the conclusion that the month directory was pretty unnecessary. What I decided on was the folder structure Year-MM.YY Event Name. 

![New Photo Structure]( {attach}photo_list.png)

This gives me a much easier way to visualize my photos by event name rather than poking through folders by month.

My Hazel workflow is fairly simple, but takes care of everything in one rule. I've set up a few exceptions for photo types that don't need to be sorted, such as screenshots or other PNG files. I also have rules set up for fun projects like my ["photo a day"]( /2014/01/05/organizing-special-photos-with-hazel ).

![Hazel Rule]( {attach}photos_hazel.png)

Finally once photos are sorted, I will manually go in and individually name all of the events that were created. This makes it much easier to search for events in the future. The next step in my process here is to tag photos. The one feature I do miss about iPhoto was the facial recognition. Since I haven't found a way to do facial recognition outside of Aperture or iPhoto, I will manually go in and tag photos with the names of those in the photos. This has been very useful when I want to find photos of people in certain contexts. For example,  the tags `me`, `office`, `dublin` will give me photos of myself in the Dublin office, but not San Francisco.

[exportiphoto]: https://github.com/BMorearty/exportiphoto

## Consumption and Sharing

In Mac OS X, I have three ways that I view my photos. The first, and most basic is Finder.  The Cover Flow view in Finder is actually a great way to quickly go through photos and get the ones that you want. When I'm wanting to share my photos with others, I use the [Dropbox Photos](https://www.dropbox.com/photos) page. As a quick way to share a select number of photos quickly, I've still found this to be the best way. For general viewing and pruning of photos I don't want, I've been using a not so well known app called [Lyn](http://www.lynapp.com). It has some nice features for sharing to multiple services, but what I really like about it is that it'll just watch a folder and display the photos in that folder. Lyn will also let me see all of the metadata about the photos, including a map if there is GPS information. Lastly, on the rare occasion that I want to edit my photo, I will import the photo into Aperture. For the same reasons I dislike iPhoto, I dislike Aperture. I will typically import the photo, edit it, and then export back into Dropbox.

![Lyn.app]( {attach}lyn.jpg)

On iOS, I have two primary apps that I use to view my photos. The first, unsurprisingly, is the Dropbox app. For quick viewing and sharing, I will use Dropbox since that's where all of my photos live. As a Photos app replacement, I use [Unbound][unbound]. What's great about Unbound is that it treats folders in your Dropbox account like albums. Since my photos are organized this way anyways, I get perfectly created albums that I can view and even cache to my phone for offline viewing.

![Dropbox and Unbound]( {attach}unbound_dropbox.jpg)

## The Future ##

Dropbox has been doing a great job improving the photo experience. Photo organization is a very personal thing and trying to solve this for the majority is not an easy task. Many companies are trying to do this, and so far there has been no clear winner. As much as I love my folder organization, I would really like to get to a point where I don't even have to worry about where my photos are. The metadata of the photos should be enough for an application or website to organize the photos for me.

I mentioned this earlier, but one other thing I would really like to see is a 3rd-party app that does facial recognition and applies tags or some other bit of metadata to the file. Tagging my photos with peoples' names is by far the most manual part of my photos workflow, but also one of the most important to me.

[unbound]: http://unboundapp.com
