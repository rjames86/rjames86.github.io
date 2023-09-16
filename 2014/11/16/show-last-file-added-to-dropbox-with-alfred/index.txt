Title: Show Last File Added to Dropbox with Alfred
Date: 2014-11-16
Modified: 2014-12-28
Category: Tech
Tags: alfred, scripting
Author: Ryan M
Summary: To continue on yesterday's post, revealing files in the Finder can be very useful. One thing that I find myself doing daily is moving into a particular folder in my Dropbox account once I've used the Alfred "move" action or when a new file has been added to my account.

*Update 2014-12-28*

I realize now that simply revealing the file isn't as useful as performing actions on the file. There are also occasions when I want to see the last 5 files added, not just the most recent. I've converted the workfow to now be a script filter.

![Show Recently Added in Dropbox]({attach}recentlyadded.png)

I've updated the download link below to be the latest Alfred workflow. The old version is still available with an empty keyword. 

Enjoy!

----


To continue on [yesterday's post][yesterday], revealing files in the Finder can be very useful. One thing that I find myself doing daily is moving into a particular folder in my Dropbox account once I've used the Alfred "move" action or when a new file has been added to my account.

How many times have you see this notification and wondered what file it was and where on earth it is in your Dropbox account?

![dropbox_notification]({attach}dropbox_notification.png)

Similar to revealing the last file added to my Dropbox folder, I can show the file last added in my Dropbox account. The only difference here is that my two Dropbox folders combined (work and personal) amount to about 150,000 files. Listing off all those files and sorting them by Date Added would take far too long. Instead, I can take advantage of `mdfind`, which is the command line version of Spotlight.

	:::bash
    DROPBOX_WORK=$(python -c "import json;f=open('$HOME/.dropbox/info.json', 'r').read();data=json.loads(f);print data.get('business', {}).get('path', '')")
    DROPBOX_PERSONAL=$(python -c "import json;f=open('$HOME/.dropbox/info.json', 'r').read();data=json.loads(f);print data.get('personal', {}).get('path', '')")
    DROPBOX="$HOME/Dropbox"
    
    LAST_ADDED=$(mdfind \
        -onlyin "$DROPBOX_PERSONAL" \
        -onlyin "$DROPBOX_WORK" \
        -onlyin "$DROPBOX" \
        'kMDItemDateAdded >= $time.today(-1)' \
        -attr 'kMDItemDateAdded' | \
    awk -F"kMDItemDateAdded =" '{print $2 "|" $1}' |
    sort -r | \
    cut -d'|' -f2 | \
    head -n1 | \
    sed -e 's/^ *//' -e 's/ *$//')

    if [ ! -z "$LAST_ADDED" ]
    then
      echo "$LAST_ADDED"
      open -R "$LAST_ADDED"
    fi

I include the paths to both the work and personal Dropbox folders if you have them (it doesn't matter if you don't) as well as the regularly named "Dropbox" folder. From there, it's a matter of getting the name and date last added for files that have been added within the last day. The result shows up almost instantly with having over 150,000 files in my Dropbox folders. 

You can download the workflow below. 

[![image]( {static}/images/alfred_extension.jpg )][download_url]  


[yesterday]: {static}../2014-11-15/2014-11-15_A_better_downloads_folder.md
[download_url]: {attach}Reveal%20last%20added%20in%20Dropbox.alfredworkflow
