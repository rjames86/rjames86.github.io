Title: A Better “Show Downloads Folder" with Alfred
Date: 2014-11-15
Category: Tech
Tags: alfred, scripting
Author: Ryan M

I've always used Alfred as a way to reveal my Downloads folder with the keyboard shortcut ⌘ ⌥ L, but that only gets me part of the way. <!-- PELICAN_END_SUMMARY -->I'm usually opening the downloads folder for a reason and so it would be handy if the file last added was already highlighted for me.

My original workflow simply looked like this

![Show Downloads Folder in Alfred]( {static}/assets/articles/better-downloads-folder/show_downloads.png "Show Downloads Folder in Alfred")

Unfortunately, listing files or using the `find` command doesn't give you the file last added. You can get away with using ctime, but not in every case. Turns out Date Added is an attribute that Mac OS X adds to every file, which meant that I could use `mdfind` to get the file that was last added. All that's left to do is print out a list of file name and date last added, sort them, and get the most recently added file from the Downloads folder. From there, its just a matter of using the `open -R` command to reveal the file

{! /assets/articles/better-downloads-folder/recent.sh !}

`mdls -name kMDItemFSName -name kMDItemDateAdded ~/Downloads/*`

Lists the name and date added for all the files in the Downloads folder

`sed 'N;s/\n//'`

Looks at the next line and removes any newlines, which puts the name and date added all on one line[^1]

`awk '{print $3 " " $4 " " substr($0,index($0,$7))}'`

Returns the name and date added in a nice format like "2014-11-15 19:36:28 "Arq.zip""

`sort -r`

Sorts the lines

`cut -d'"' -f2`

Splits the lines on a quotation mark and returns the second result (the filename)

`head -n1`

Gives the top item in the list, which is the most recently added file

`open -R`

Reveals the file instead of opening it in OS X.

You can download this workflow to reveal the last added file in your Downloads folder below.

[![image]( {static}/images/alfred_extension.jpg )][download_url]


[download_url]: {static}/downloads/OpenDownloadsFolder.alfredworkflow


[^1]: You can read a nice explanation of how the N command works in sed [here](http://stackoverflow.com/questions/6255796/how-the-n-command-works-in-sed)
