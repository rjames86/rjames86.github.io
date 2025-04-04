Title: Adding Critical CSS in Pelican
Date: 2015-09-14 07:41
Modified: 2017-01-05 20:45
Category: Tech
Tags: pelican, automation, python
Author: Ryan M

As it turns out, adding [critical css][critical css] wasn't trivial, but didn't take as much effort as I had originally thought. My site's layout doesn't contain *that* much styling, and so I simply added all of my CSS as an inline `style` tag. The tricky part, was getting Jinja to play nicely.

The first step was to generate a separate css file that only contained what was needed when you first load and see the page. I use Less as my pre-processor, and created a very small Less file that looked like this:

	:::css
	@import (inline) '../tipuesearch/tipuesearch.css';

	@import 'default_mobile.less';
	@import 'largescreens.less';

Once compiled and minimized[^1], I needed to add it to my `base.html` template.

	:::jinja
	<style type="text/css">
	{% include 'critical.css' %}
	</style>

Here is where the problem when generating my site.

	:::bash
	WARNING: Caught exception "TemplateSyntaxError: Missing end of comment tag". Reloading.

Since my minimized CSS contained `'{#'`, Jinja was interpreting this as a comment and raised an exception. While this is an easy fix by changing the Jinja environment variables within Pelican's generators.py, I didn't want to go this route since I would need to update this[^2] every time there was an update to Pelican. Instead, I wrote a Jinja extension which Pelican supports natively. 

	:::python
	# in pelicanconf.py
    from jinja2.ext import Extension

    class CustomCommentStrings(Extension):
        def __init__(self, environment):
            super(CustomCommentStrings, self).__init__(environment)

            environment.comment_start_string = '###'
            environment.comment_end_string = '/###'

    JINJA_EXTENSIONS = [CustomCommentStrings]

---

*Update 2017-01-05*

If you're using Pelican version 3.7+, you don't have to write the custom extension shown above, you can simply update the `JINJA_ENVIRONMENT` settings variable:

    :::python
    JINJA_ENVIRONMENT = {
        'comment_start_string': '###', 
        'comment_end_string': '/###'
    }

---

One thing to note here is that if you are using `{# ... #}` as comment strings in Jinja, you'll need to update them to whatever new start and end strings you define.

And success! The `critical.css` file was successfully imported and I now my critical CSS is included on page load. With this, Google now gives me a 100/100 speed score for mobile and 98/100 on desktop.


[^1]: Google suggests that you minimize critical css to reduce your file size.

[^2]: I plan on submitting a pull-request to allow manually setting Jinja environment variables.

[critical css]: http://www.smashingmagazine.com/2015/08/understanding-critical-css/
