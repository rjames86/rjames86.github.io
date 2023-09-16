Title: Publishing from Day One to Pelican with Hazel and Dropbox
Date: 2016-08-19 11:02
Category: Tech
Tags: hazel, pelican, automation, dropbox
Author: Ryan M

I'll be soon embarking on a long bike tour and was searching for a way to keep a journal of my trip but also post updates to a website. Day One was an obvious journaling choice, but with version 2, publishing isn't yet available. With a little poking around, it turned out to be fairly easy to export Day One entries and publish to Pelican (my static blog generator of choice).
<!-- PELICAN_END_SUMMARY -->

I've not been a heavy user of Day One, and with the new version, I've stopped entirely until they provide end-to-end encryption with their proprietary sync service. Journaling my bike trip isn't anything I'm worried about being out in the open, and so I'll use it to keep a log of my days on the trip. At the same time, I want to keep my friends and family up-to-date on my trip. Since I use Pelican for this site, it seemed like a reasonable choice to use it for this trip and use Github Pages as an easy, free place to host it.

The first step was getting the Pelican site set up. I used the basic quickstart and put in a custom theme that I found online. The only modifications I made was using the [photos plugin](https://github.com/getpelican/pelican-plugins/tree/master/photos) to make it easier to add galleries if I want in the future. Publishing to Github Pages is trivial. You can follow the steps [here](http://docs.getpelican.com/en/3.6.3/tips.html#publishing-to-github).

Now the fun part. Day One lets you export a journal entry as Markdown. When exported, it's compressed into a zip file which includes a folder of photos if you've included any in the journal entry. For each post, I use the export action and then upload to a folder I've created in Dropbox. I have Hazel watching this folder which will do the following:

1. Unarchive any file that appears
2. Move the unarchived contents into a new folder I unoriginally name "decompressed"

![unarchive]({static}unarchive.png)

I then have a separate rule watching "decompressed" which will

1. Move any image file type into my blog's images folder
2. Move any text file into the content folder

![move_text]({static}move_text.png)

Step 2 here requires a little bit of extra work. Day One has some weird formatting issues and I also need to update the image urls in the entry to match what Pelican expects. The script isn't my finest, but it takes care of everything

{! cleanup_dayone.py !}
 
Now the file is cleaned up and in the right place. We can now publish and push to Github.

{! publish.sh !}

That's it! You can see the posts and follow my bike tour at [http://rjames86.github.io](http://rjames86.github.io)
