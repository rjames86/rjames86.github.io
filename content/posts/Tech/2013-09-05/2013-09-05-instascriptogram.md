Title: Instascriptogram. Post Instagram pics to Scriptogr.am
Date: 2013-09-05
Category: Tech
Slug: instascriptogram
Tags: dropbox, scripting, ifttt, photos
Modified: 2014-11-19
Author: Ryan M

**[Update 2014-11-19]**
I've since moved off of scriptogr.am. The service wasn't working for a long time and doesn't seem to be in active developement. I ended up moving that blog over to a static blog with Pelican similar to this one.

----
<!-- PELICAN_BEGIN_SUMMARY -->
Since moving to Dublin, my girlfriend and I have wanted to keep our friends and family up-to-date on everything we've been doing. I recently bought the new Olympus E-P5 and have been taking a lot of pictures. So that everyone knows what we're doing, we decided to share a [Scriptogr.am][scriptogram] blog and post pictures of our adventures. 
<!-- PELICAN_END_SUMMARY -->  

Sometimes it's quick and easy to snap a picture on Instagram and share with all your friends, but my parents and family aren't on Instagram, but they know to follow my blog for updates. Instead of having to manually pull the pics down, write up a post and publish it, I used a combination of IFTTT, Dropbox and my server at Macminicolo.net to do all the work for me.

The magic starts at IFTTT. I have a [recipe][recipe] that watched for a particular tag when I post to Instagram. If that tag exists, a text file is saved to my Dropbox account. I have a cron running once an hour[^1] to run the script and check for any new files.

One of the only complaints about Scriptogr.am has been that I have to manually hit a publish button before posts will go live. But with their API, the posts are immediate[^2]. Now, all of my Instagram adventures (and my girlfriend's) can be posted to our blog for friends and family to follow. Once the post is made, I get a Pushover notification letting me know that a post was made by either me or my girlfriend.

![pushover_instascriptogram]( {attach}pushover_instascriptogram.jpg )

If you're interested in the script, it can be found on Github [here][github]. An example of the posts being made can be found at our travel blog [keephouseadventures.com][blog]

[scriptogram]: http://www.scriptogr.am
[recipe]: https://ifttt.com/recipes/115652
[github]: https://github.com/rjames86/instascriptogram
[blog]: http://keephouseadventures.com/posts/2013/Sep/03_12_44/instagram-pic-for-tuesday-sep-03/

[^1]: I tried using Hazel for this, but I kept getting errors since I wasn't actually processing the file. Any suggestions on this, please let me know!  

[^2]: Like what you get from apps like Byword
