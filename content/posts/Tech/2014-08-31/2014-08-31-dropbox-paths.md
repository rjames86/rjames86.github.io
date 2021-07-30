Title: Global Shell Variables for Dropbox Paths
Date: 2014-08-31
Category: Tech
Tags: bash, scripting, Dropbox
Author: Ryan M

I have multiple computers running Dropbox, all of which have different folder paths to where the Dropbox folder is located. I wanted to have a universal way to find and navigate to the folders regardless of what computer I was on.
<!-- PELICAN_END_SUMMARY -->  

In most cases, setting a variable to your Dropbox path is relatively easy. You could set your .bashrc to look something like this

	:::bash
	DROPBOX_PERSONAL=$HOME/Dropbox

But this fails in a few situations, all of which apply to me on one or more of my computers

- Multiple Dropbox accounts on one computer (Personal and Business accounts)
- Dropbox isn't located in my home folder

If you're running Dropbox version 2.8 or higher (you should be anyways), there's a json file that tells you where your Dropbox folders are located. The json looks like this:

	:::bash
	{
		"personal": {
			"path": "/Users/username/Dropbox (Personal)",
			"host": 1234
		},
		"business": {
			"path": "/Users/username/Dropbox (Business)", 
			"host": 5678
		}
	}

What this means is that you can set global variables using this information in your .bashrc or .bash_profile so that you always know where your Dropbox folder is

	:::bash
	DROPBOX_WORK=$(python -c "import json;f=open('$HOME/.dropbox/info.json', 'r').read();data=json.loads(f);print data.get('business', {}).get('path', '')")
	DROPBOX_PERSONAL=$(python -c "import json;f=open('$HOME/.dropbox/info.json', 'r').read();data=json.loads(f);print data.get('personal', {}).get('path', '')")

Now all you have to do is reference your Dropbox folders with `$DROPBOX_PERSONAL` or `$DROPBOX_WORK`.
