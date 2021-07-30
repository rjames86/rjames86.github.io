Title: Exploring Pelican: Automation Part 1
Date: 2013-12-29
Category: Tech
Tags: scripting, efficiency, pelican
Slug: exploring-pelican-automation
Author: Ryan M
Series: Exploring Pelican
Summary: Pelican is a great python-based static blog generator. After a few months using it, I’ve decided to automate the content generation as much as possible.

It's been a few months now since I switched from [Mynt][mynt] to [Pelican][pelican] as my static blog generator and so far I've been very happy with the switch. It's been a learning process along the way, but I've come to the point where I'm comfortable enough with it and want to start customizing and automating.

[mynt]: http://mynt.mirroredwhite.com
[pelican]: http://blog.getpelican.com

## Customization ##

I haven't done much yet in terms of customization quite yet, but I'm adding little bits every day.  

### Original Files ###

I recently updated Pelican to the newest version 3.3. The part that was new to me here was that you have the option to keep the original file in your output directory.

	:::python
	# Set to True if you want to copy the articles and pages in their original format (e.g. Markdown or reStructuredText) to the specified OUTPUT_PATH.
	OUTPUT_SOURCES = True

**Update 2014-02-25:** Turns out this was a bug. It's been since fixed. See the thread [here][github] on github. 

[github]: https://github.com/getpelican/pelican/pull/1183

I'm not entirely sure if it's a bug or something I was doing wrong, but I noticed that instead of creating an index.txt for every index.md file, it would create a directory called index.txt and then place the original markdown file within it. I did some poking around in the source code and found a slight issue with the `copy` function within the util.py file. It was checking if any destination existed, and if not, it would create a new directory.

	:::python
    if not os.path.exists(destination_):
        os.makedirs(destination_)

I made a couple of changes to prevent this from happening. The first was that I added an additional argument to the function called `is_file` and then added this to the destination check

	:::python
	def copy(path, source, destination, destination_path=None, is_file=False):
	...
	if not os.path.exists(destination_) and not is_file:
        os.makedirs(destination_)

Finally, in generators.py, I added the argument where the copy function is called in `_create_source` in the `SourceFileGenerator` class.

	:::python
	copy('', obj.source_path, dest, is_file=True)

Now that the files are being generated correctly, I used the tip by Gabe Weatherhead over at [Macdrifter][macdrifter_pelican] to add a link to the original file for every post. You can see an example of this post at the bottom of the page.

### Automatic Posting to App.net ###

App.net's new Broadcast platform is pretty cool. I've subscribed to a few people already and I like the idea of having a way to broadcast each post that's made. Pelican doesn't have a great way to detect new posts, so I'm playing with my own solution by keeping track of every post and comparing.

In my Fabric file, I created a function to check for new posts and then use the App.net Broadcast API to make a post

	:::python
    def adn():
    	current_posts = util.current_posts()
    	post_history = pickler.load_old_results('lib/posts.pkl')
    	new_posts = list(set(current_posts) - set(post_history))

    if new_posts:
        for post in new_posts:
            get_adn = util.ADN(POST_PATH + post)
            get_adn.post()
        pickler.store_results('lib/posts.pkl', current_posts)

I get the current posts by simply listing the contents of the posts directory and then compare to what was previously stored the last time a new post was made. I keep this is a file called lib/util.py, which explains why I have to call `os.path.dirname` twice.

	:::python
    def current_posts():
        post_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'posts')
        return [f for f in os.listdir(post_path) if not f.startswith('.')]

This seems to be the most reliable solution since it won't send broadcasts if I edit a file. Finally, when the publish function is called from my fabfile, I call `adn()`.

## Automation ##

I'm traveling a lot these days, which means that sometimes I only have my iPad or iPhone with me. I'd still like to easily create posts without having to write up the post, log in via Prompt, commit and push. I went with a setup fairly similar to [Evan Lovely][evanlovely] and use Hazel to watch for new posts within a directory. 

My Hazel workflow relies on an additional piece of metadata in my posts instead of just the file itself. This prevents any accidental posts and also lets me put whatever file I want in the folder. The file needs to pass the following script:

	:::python
	import markdown
	import sys
	import codecs
    
	f = codecs.open(sys.argv[1], mode='r', encoding='utf-8').read()
	md = markdown.Markdown(extensions = ['meta'])
	md.convert(f)
    
    if md.Meta.get('hazel'):
    	sys.exit(0)
    else:
    	sys.exit(1)

As long as the piece of metadata "hazel" exists in any of my files, Hazel  moves the file into my Pelican project folder and my publish script takes over.

That's it for now! I'll keep iterating on the process and make things better.

[macdrifter_pelican]: http://www.macdrifter.com/tag/pelican.html
[evanlovely]: http://www.evanlovely.com/notes/about-this-jekyll-site/
