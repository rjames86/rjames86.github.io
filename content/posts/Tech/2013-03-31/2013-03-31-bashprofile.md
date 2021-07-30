Title: Your .bash_profile everywhere
Date: 2013-03-31
Category: Tech
Slug: bashprofile
Tags: dropbox, efficiency, bash
Author: Ryan M

I have two computers, one for work and one for personal. I keep mostly everything separate, but one thing I want to always have with me is my terminal environment and aliases. With Dropbox, I can not only access, but edit my .bash_profile from anywhere *without* using symlinks.
<!-- PELICAN_END_SUMMARY -->  

The first thing to do is figure out where you want to keep your .bash_profile in your Dropbox account. I keep mine in a folder called Sync that's shared between my work and personal Dropbox accounts. To move your .bash_profile, use the following command in Terminal:

    mv ~/.bash_profile ~/path/to/Dropbox/.bash_profile  

Once you've moved it here, create a new .bash_profile in your home directory and add the single line:

	source ~/that/path/to/.bash_profile

Thats it! From now on, just point the local .bash_profile to the one location in your Dropbox folder.



