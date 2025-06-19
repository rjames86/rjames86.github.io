Title: Create a Scratchpad with Alfred
Date: 2013-12-28
Category: Tech
Tags: alfred, automation
Summary: I created a quick Alfred workflow that takes the contents of my clipboard and opens a new file in Sublime Text (or Text Edit).
Author: Ryan M

I always have an empty doc open on my computer as a place to quickly paste in some text. It's never something I need to save and I'll never miss it if I happen to lose it. The only problem is that it's slow recreating this scratchpad file or find it each time I need it. 

I created a very simple workflow that takes the contents of my clipboard and opens a file in a text editor of my choice. The Alfred workflow can be triggered in one of two ways. The first is with the keyboard shortcut "hyper"-s[^1]. The second way is simply typing "scratchpad" into Alfred. 

![scratchpad_alfred]({static}/assets/articles/alfred-scratchpad/scratchpad_alfred.jpg)

I have it set to save a file in my Home folder called ".scratchpad" and then open the file in Sublime Text. Right now, the workflow will check for Sublime Text version 3, then version 2 and if neither exist, it will open the scratchpad in Text Edit. 

![scratchpad_example]({static}/assets/articles/alfred-scratchpad/scratchpad_example.jpg)

You'll need the Alfred Powerpack to use this workflow. If you already have it, you can download it with the link below. 

[![image]( {static}/images/alfred_extension.jpg )][download_url]  

[^1]: command-option-control-shift mapped to my caps lock key. You can read more [here][hyper] on how to make a hyper key

[hyper]: http://brettterpstra.com/2012/12/08/a-useful-caps-lock-key/
[download_url]: {static}/assets/articles/alfred-scratchpad/Scratchpad.alfredworkflow
