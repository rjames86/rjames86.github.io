Title: Instagram for Slogger
Date: 2014-09-04
Category: Tech
Tags: scripting, efficiency, slogger, dayone, photos
Slug: instagram-slogger
Author: Ryan M

In early 2013, I discovered Slogger and loved the idea of journalling about more than just what I had to say. What I was listening to at a given time is just as important as what I was thinking. However, there wasn't an ideal way to log Instagram posts without other dependencies, and so I took a stab at writing my first plugin.
<!-- PELICAN_END_SUMMARY -->  

--- 

*Update*

As of June 2016, Instagram has changed their API and no longer allows this script to work. Sorry :(

---

I didn't know ruby and quickly learned how bad some API documentation can be, but I wanted this plugin more than all the others. After fiddling with it for an evening, I was able to log Instagram posts with more than just a photo, including:

- number of likes
- comments
- date of post, not the date Slogger ran
- location data (including place name if you used Foursquare checkin)

The last point is by far my favorite. I can look at a map over the last year and see all the Instagram photos I've taken and where I took them

 ![Instagram map]( {attach}dayonemap.png)

I also wanted to import photos that I had already taken. The plugin now will let you set `backdate: true` and will log the last 20 photos that you had posted on Instagram. Once it's finished, it'll automatically set itself to false to prevent duplicate posts[^1].

Setup is fairly straight forward. I create a local server, which runs you through the Instagram OAuth flow. After you've finished, you simply paste in the access token, and it'll run from there

	:::bash
	> ./slogger -o instagram
	Initializing Slogger v2 (2.1.14)...
	08:01:18      InstagramLogger: Instagram requires configuration, please run from the command line and follow the prompts

	------------- Instagram Configuration --------------

	Slogger will now open an authorization page in your default web browser. Copy the code you receive and return here.

	Press Enter to continue...

Last night I finally did a pull request and it went live this morning. You can check out and download the latest Slogger on [Github][github]. If you find any issues or bugs, please send them my way. Enjoy!

 ![Instagram map]( {attach}dayone.png)

[github]: https://github.com/ttscoff/Slogger

[^1]: It looks like in the newest version of Slogger, you can find and delete duplicate posts.
