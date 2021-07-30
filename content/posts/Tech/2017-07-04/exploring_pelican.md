Title: Exploring Pelican: Part 2
Date: 2017-12-03 15:22
Category: Tech
Tags: scripting, efficiency, pelican
Slug: exploring-pelican-automation-part-2
Author: Ryan M
Series: Exploring Pelican
status: draft

If I spent half as much time posting blog posts as I did actually messing around with Pelican, I'd have a lot more posts by now. I've been using Pelican now for almost 4 years and have constantly been tweaking it. I've created a lot of fun things that make the overall use of Pelican much nicer and make it easier to create posts and maintain a clean folder structure.
<!-- PELICAN_END_SUMMARY -->

Back in 2013, I [wrote about][pelican automation] the automation I was doing with Pelican. I don't think I'm using any of that now, but have found some new ways to not necessarily automate, but just make Pelican nicer to use. Here are a few of the things I've been up to.

[pelican automation]: {static}../2013-12-29/Exploring-Pelican-Automation.md

## Code Snippets ##

I post a lot of code snippets in my posts. Writing (or even pasting) in code into Markdown isn't my favorite. If I have to edit the snippet, I almost always re-open the post in Sublime Text, edit, and then go back to my editor. Embedding gists is convenient, but I don't like the way that embeds are done and it's just one more place for me to have to go. What I ended up doing was creating a Jinja extension where I could define my own syntax for adding in any text from a separate file. Now, instead of writing any code in my posts, I can use the syntax `{ ! my_snippet.py ! }`  for inserting a code snippet. This also cleans up the posts a lot.

## Custom Markdown Reader ##

The first step was to write a Jinja preprocessor extension that would parse my new syntax. 

{! /../lib/gist.py !}

This was a lot less work than it appears. This same structure exists already for Pelican's `{static}` and `{attach}`.

{! /../plugins/code_replacement/code_replacer.py !}

## JSON Feed ##

## Mixed Content in the Same Directory ##

{! folder_structure.txt !}

## Drafts Category ##

	:::jinja
{! /../theme/templates/drafts.html !}


[mixed content]: http://docs.getpelican.com/en/stable/content.html#mixed-content-in-the-same-directory

