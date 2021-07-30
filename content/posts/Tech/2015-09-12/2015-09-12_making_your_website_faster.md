Title: Improving Your Site's Load Times
Date: 2015-09-12 01:15
Category: Tech
Tags: pelican, javascript, scripting
Author: Ryan M

While reading through my RSS feeds the other night, I came across [this][onetapless] article from One Tap Less about what he did to improve load times on his site. My first thought was,  "I use a static site, I don't need to worry about this" and dismissed it. Then I figured, why not just try out my site on Google's [PageSpeed Insights][pagespeed]. Turns out, I had some work to do.
<!-- PELICAN_END_SUMMARY -->

When I initially ran the test, this site came back with a score of around 41/100 for both desktop and mobile. I would have been fine leaving it, but that was pretty bad. Google does a great job telling you what things need to be improved, even down to the specific files causing problems.

![file_specific]({static}file_specific.png)

My first task was "eliminating render-blocking JavaScript and CSS." I was lazily loading all of my JavaScript in the `<head>` tag, so this was as simple as moving that to the bottom of the page. Google also suggested using the `async` attribute.

	:::html
	<!-- Initial setup -->
	<!DOCTYPE html>
	<html lang="{{ DEFAULT_LANG }}">
	<head>
		<script async src="{{ SITEURL }}/theme/js/main.js" type="text/javascript"></script>
	  ...
	</head>
	
	<!-- New setup -->
	...
		<script async src="{{ SITEURL }}/theme/js/main.js" type="text/javascript"></script>
	</body>
	</html>

Eliminating render-blocking CSS was a little more tricky. Google suggests inlining [critical CSS][critical_css]. I haven't taken the time to figure out which CSS that would require and how this would change my workflow. For now, I've taken their suggestion and load my CSS at the bottom of the page using a `<script>` tag.

*\[Update 2015-09-14\]*: I figured it out. You can read how I added the critical css [here]({static}../2015-09-14/2015-09-14-critical_css.md)


	:::javascript
	<script>
      var cb = function() {
        var l = document.createElement('link'); l.rel = 'stylesheet';
        l.href = "{{ SITEURL }}/theme/css/style.css";
        var h = document.getElementsByTagName('head')[0]; h.parentNode.insertBefore(l, h);
      };
      var raf = requestAnimationFrame || mozRequestAnimationFrame ||
          webkitRequestAnimationFrame || msRequestAnimationFrame;
      if (raf) raf(cb);
      else window.addEventListener('load', cb);
    </script>

Ok. Easy stuff done. This put my site up into the 50's range. Good, but still not great. Let's tackle the one that's lowering my score the most: gzip compression and caching.

I host my blog at the wonderful [macminicolo.net](http://macminicolo.net), which means I control the server and have to do my own optimizations. Turns out, this really wasn't that hard to do. Here's how to easily enable compression in Apache.

	# Always back up your config file before changing a bunch of stuff
	sudo emacs /etc/apache2/httpd.conf

	# Make sure this is enabled
	LoadModule deflate_module libexec/apache2/mod_deflate.so

    <IfModule mod_deflate.c>

        # Restrict compression to these MIME types
        AddOutputFilterByType DEFLATE text/plain
        AddOutputFilterByType DEFLATE text/html
        AddOutputFilterByType DEFLATE application/xhtml+xml
        AddOutputFilterByType DEFLATE text/xml
        AddOutputFilterByType DEFLATE application/xml
        AddOutputFilterByType DEFLATE application/x-javascript
        AddOutputFilterByType DEFLATE text/javascript
        AddOutputFilterByType DEFLATE application/javascript
        AddOutputFilterByType DEFLATE application/json
        AddOutputFilterByType DEFLATE text/css

        # Level of compression (Highest 9 - Lowest 1)
        DeflateCompressionLevel 9

        # Netscape 4.x has some problems.
        BrowserMatch ^Mozilla/4 gzip-only-text/html

        # Netscape 4.06-4.08 have some more problems
        BrowserMatch ^Mozilla/4\.0[678] no-gzip

        # MSIE masquerades as Netscape, but it is fine
        BrowserMatch \bMSI[E] !no-gzip !gzip-only-text/html

        <IfModule mod_headers.c>
            # Make sure proxies don't deliver the wrong content
            Header append Vary User-Agent env=!dont-vary
        </IfModule>
    </IfModule>

Save and restart Apache

	sudo /usr/sbin/apachectl restart

You can test to be sure it's working by using `curl` on a file that matches any of the above content types. You should see `Content-Encoding: gzip` in the response headers.

	:::bash
	curl -I -H 'Accept-Encoding: gzip,deflate' https://ryanmo.co/theme/js/main.js


	HTTP/1.1 200 OK
	Date: Sat, 12 Sep 2015 20:38:24 GMT
	Server: Apache/2.4.10 (Unix) PHP/5.5.20 OpenSSL/0.9.8zd
	Last-Modified: Sat, 12 Sep 2015 02:47:24 GMT
	ETag: "38169-51f83da1c0700-gzip"
	Accept-Ranges: bytes
	Vary: Accept-Encoding,User-Agent
	Content-Encoding: gzip
	Cache-Control: max-age=2592000
	Expires: Mon, 12 Oct 2015 20:38:24 GMT
	Content-Type: application/javascript

Next is content caching. This is also something to edit in the httpd.conf file for Apache. Google suggests at *least* 7 days for default caching, and up to a year for content that doesn't change often.

	:::bash
	# Make sure this is uncommented
	LoadModule expires_module libexec/apache2/mod_expires.so

    ## EXPIRES CACHING ##
    <IfModule mod_expires.c>
        ExpiresActive On
        ExpiresByType image/jpg "access plus 1 year"
        ExpiresByType image/jpeg "access plus 1 year"
        ExpiresByType image/gif "access plus 1 year"
        ExpiresByType image/png "access plus 1 year"
        ExpiresByType application/x-font-ttf "access plus 1 year"
        ExpiresByType text/css "access plus 1 month"
        ExpiresByType application/javascript "access plus 1 month"
        ExpiresByType image/x-icon "access plus 1 year"
        ExpiresDefault "access plus 7 days"
    </IfModule>
    ## EXPIRES CACHING ##

At this point, I was getting into the mid to high 80s for my score. Awesome. At this point, I could probably stop and be satisfied with the results. The remaining suggestions were easy, so I kept going. The first was to minimize all of my CSS and JavaScript. Easy. I just hit that checkbox in CodeKit and moved along. I did take one additional step here and took advantage of CodeKit's ability to combine JavaScript files into a single file by adding a header to my main JavaScript file.

	# @codekit-prepend "../js/jquery-1.10.1.min.js", "../js/bigfoot.min.js";

Lastly, Google suggested that I compress my images. They were even nice enough to provide a zipped file of all your CSS, JavaScript and images compressed for you. If I don't have to do the work, then I won't. I downloaded the file and replaced all my images with the ones they gave me. In the future, I'll be using [ImageOptim][imageoptim] to optimize the images on my site.

My final score check: 91/100 on mobile and 97/100 on desktop! I think I can call that a success. Honestly, when trying to load my site on different devices, I didn't notice a significant increase. That being said, at least I'll be in Google's good graces for being a good web citizen, and I'll avoid any risk of them down-ranking my site for doing things incorrectly. I still want to take advantage of the critical CSS at some point, but I can leave that for another day.

[onetapless]: https://onetapless.com/whats-new-one-tap-less
[pagespeed]: https://developers.google.com/speed/pagespeed/insights/
[critical_css]: http://www.smashingmagazine.com/2015/08/understanding-critical-css/
[imageoptim]: https://imageoptim.com
