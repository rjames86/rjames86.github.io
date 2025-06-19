Title: Find images with No Exif Dates
Date: 2014-08-01
Category: Tech
Tags: bash, automation, exiftool, photos
Author: Ryan M

My Dropbox folder is full of images claiming to be "missing dates." [^1] Some of these photos were thumbnails or images from DayOne that didn't necessarily need dates, but others were real photos that for whatever reason didn't have dates that Dropbox recognized.
<!-- PELICAN_END_SUMMARY -->  

![Carousel Missing Photos]( {static}/assets/articles/find-images-no-exif-dates/carousel_missing.png)

I did some poking around, and found that there were a couple of different reasons why my photos in Dropbox weren't displaying dates:

- The DateTimeOriginal exif tag was missing entirely
- The DateTimeOriginal was set to 0000:00:00 00:00:00

With the magic of [exiftool][exiftool], I found a way to find all the photos in my Dropbox folder that were missing dates and output the results to a CSV.

	:::bash
	exiftool -filename -r -if '(not $datetimeoriginal or ($datetimeoriginal eq "0000:00:00 00:00:00")) and ($filetype eq "JPEG")' -common -csv > ~/Dropbox/nodates.csv

This will give you a CSV with all of the common file information for the images. 

![CSV of Missing Photos]( {static}/assets/articles/find-images-no-exif-dates/csv.png)

At this point, you'll need to decide how you'll want to fix these photos. From what I have seen so far, the best exif tag to go on is `-filemodifydate`, but you'll probably need to figure that out on your own. If you want to fix any photo that matches the above criteria, you can do something like this

	:::bash
	exiftool `-datetimeoriginal<filemodifydate` -r -if '(not $datetimeoriginal or ($datetimeoriginal eq "0000:00:00 00:00:00")) and ($filetype eq "JPEG")' ~/Dropbox


[^1]: 2965 photos to be exact.

[exiftool]: http://www.sno.phy.queensu.ca/~phil/exiftool/
