Title: [Updated] Log Your Instagram Posts with Slogger
Date: 2013-05-08
Category: Tech
Slug: instagram_and_slogger
Tags: slogger, dropbox, dayone, photos
Author: Ryan M

--- 

**Update 2016-06-23**

As of June 2016, Instagram has changed their API and no longer allows this script to work. Sorry :(

*Update 2014-09-04*

I recently submitted a new plugin that now comes with Slogger which uses the Instagram API. You can check out my post with more information [here][newpost].

[newpost]: {filename}2014-09-04-instagram-slogger.md

----

<!-- PELICAN_BEGIN_SUMMARY -->
I've received a few questions about [this][recipe] IFTTT recipe which logs my Instagram posts to Day One. There are a few others floating out there, but there are a couple of things that I wanted to have:
<!-- PELICAN_END_SUMMARY -->  

* The Day One entry date is the date the picture was taken
* The caption is saved in the journal entry
* Ignore duplicate posts if I also posted to Twitter

The last point assumes that I'm also using the default Twitter logger. If you want to ignore all of your Instagram tweets, add the following to be on line 112 in the twitterlogger plugin:

	:::ruby
	break if tweet_text.include? 'instagram'
	 
You can download the Instagram IFTTT Slogger extension [here][instagram_ifttt]. Simply add it to your plugins directory and run the following once to set up the slogger_config file:

	:::bash
	./slogger -o instagram_ifttt

You'll need to set the location of your IFTTT slogger directory. The plugin will check for any text files and then automatically move them into a "logged" folder once they've been added to Day One. 

![image]( {static}/assets/articles/instagram-and-slogger/dayone_instagram.jpg )

[instagram_ifttt]: {static}/assets/articles/instagram-and-slogger/instagram_ifttt.rb
[recipe]: https://ifttt.com/recipes/62754
