Title: Download Pinboard Bookmarks with OS X Tags
Date: 2014-12-23
Category: Tech
Tags: scripting, python, projects
Slug: pinboard-downloader
Author: Ryan M

For the last few years, I've been using Brett Terpstra's [Pinboard to Openmeta][pinboardopenmeta] to save my Pinboard bookmarks locally. In the last few months, I've been spending more and more time trying to fix issues to get it to run reliably. Since this is something that I use often, I figured it was worth just re-writing it myself.
<!-- PELICAN_END_SUMMARY -->  
The script is a slightly simpler version of the original, but the core functionality is the same. Each bookmark is saved as a webloc file and apply any OS X tags to the file. This can be paired with an [Alfred workflow][workflow] to easily search by title or tag.

You can download the download-pinboard project [here][githubdownload]. Feel free to check out the Github project [here][github].

### Setup ###

Create a settings file

	:::bash
	cp settings.py{.example,}

with the following information

	:::python
    _PINBOARD_TOKEN = 'YOUR TOKEN HERE'
    _SAVE_PATH = HOME + '/Bookmarks/'

In settings.py set your Pinboard token and the path where you want your bookmarks to be saved. Your token can be found at [https://pinboard.in/settings/password](https://pinboard.in/settings/password). The path must exist where you save your bookmarks and must end with a trailing /.

### Running the Script ###

To start the script, you can simply do

    python main.py

#### Optional arguments  ####

`-v, --verbose` Shows output as stdout  
`-t` Filters the bookmarks you want to download by tag. You can pass multiple -t tags, but no more than 3. Multiple tags are AND not OR  
`--reset [optional num of days]` Resets your last updated time. If you don't specifiy a number, it will reset to 999 days.  
`--skip-update` Lets you bypass the last downloaded time. Nice for redownloading everything.  

### Notes and Todo ###

I have a very small number of bookmarks (~150) and so I don't know if there will be any issues with a really large library. If you have one, and run into problems, please let me know and I'll happily look into it.

----


[pinboardopenmeta]: http://brettterpstra.com/2011/04/02/mirror-your-pinboard-bookmarks-with-openmeta-tags/
[workflow]: {static}/downloads/pinboard-downloader/Bookmarks.alfredworkflow
[githubdownload]: https://github.com/rjames86/download_pinboard/archive/master.zip
[github]: https://github.com/rjames86/download_pinboard
