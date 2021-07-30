Title: Organizing Special Photos with Hazel
Date: 2014-01-05
Category: Tech
Tags: hazel, efficiency, photos
Author: Ryan M

Nearly all of my photos are sorted based on year, month and day. Hazel easily takes care of of this for me, but occasionally I will have projects where photos need to be excluded or organized in a different way. With Hazel, I can still account for these special cases with extra bits of metadata.
<!-- PELICAN_END_SUMMARY -->  

This may not come in handy to anyone, but I thought it would be worth showing some of the creative ways that Hazel can be used to organize your files based on more than just creation/modification time or file type.

In late May 2013, I decided I wanted to do one of those time lapse videos where you take a picture of yourself in front of the camera every day. At first, the hardest part was just remembering to take the picture each day. Once I was in the routine, I started to find the task monotonous to pull the photo from my Dropbox folder, rename it to YYYY-MM-DD.jpg and then move it into a special folder I had creatively named "Picture a Day." Hazel was already taking care of my general photo organization, but I wanted to ensure that these photos got organized specifically so I started digging into the special traits of these photos. I quickly found a few default options in Hazel that would help me do this:

- Device make
- Pixel width/height
- Content creator

I was always using Camera+ for these photos because of the grid and level features. It allowed me to align my face in the same place in the photos. Since I always used the front camera, the dimensions of the photos remained the same. After playing around, here is the Hazel rule I came up with

![Hazel Picture a Day]( {attach}hazel_picture_a_day.png)

Another key piece here is the datestamp token. The rule watches for Dropbox's Camera Uploads filename format YYYY-MM-DD HH.MM.SS.jpg. This wouldn't be necessary except for that this token then becomes useful in the actions portion. I can take that token and rename the file based on the token to simply YYYY-MM-DD.jpg since I don't care about the hour the photo was taken. What's great about the token is that this will prevent accidental naming of the file if I happen to upload it the next day or I'm flying between Ireland and the US and date times get messed up.

While this rule is fairly specific, it's saved me a lot of time having to organize the photos manually. 



