Title: Show Time in Multiple Time Zones with TextExpander
Date: 2014-05-10
Category: Tech
Tags: bash, automation, textexpander
Author: Ryan M

I'm really bad at converting a time to other timezones. Now that the company I work for has offices in multiple countries, scheduling has become much more difficult. In an effort to eliminate the need for people to convert times themselves, I wrote a TextExpander snippet to take care of it for me.
<!-- PELICAN_END_SUMMARY -->  

There are tons of tools out there that show you what time it is in other parts of the world. One thing that isn't as readily available is a quick way to tell me what time it would be in California if it's 3:00pm in Dublin. I decided to write a quick TextExpander snippet that would let me pick the time and then it would output the time in all of my chosen time zones. 

The first step is to choose the time zones that you want to appear. In my case, I chose the following since we have offices in these locations:

- Europe/Dublin
- America/Los_Angeles
- America/Chicago

Now I need to convert a chosen time to all of these time zones. This can be done using the `date` command in bash. Here's a quick example to try in the Terminal:

    TZ=Europe/Dublin date -jf "%H:%M %z" "$(date "+%H:%M %z")" "+%H:%M %Z"
   
   - TZ lets you choose the time zone for the `date` command
   - \-f tells `date` the format to expect for the input
   - \-j tells `date` to not change the date allowing the -f flag to convert a time
   - "$(date "+%H:%M %z")" just gives the current date that looks like HH:MM +0100
   - "+%H:%M %Z" is the output format

This gives you the following result:

04:52 IST

Now to do this for multiple time zones:

	:::bash
	timezones=( "America/Los_Angeles" "America/Chicago" "Europe/Dublin")
	
	for zone in ${timezones[@]}
	do
    	TZ=$zone date -jf "%H:%M %z" "$(date "+%H:%M %z")" "+%H:%M %Z";
	done

Which gives:

08:55 PDT  
10:55 CDT  
16:55 IST  

Lastly, let's add in some TextExpander input methods, and we have a way to use this with whatever time we want:

	:::bash
	#! /bin/bash
	
	/* 
	Enter a time using 24H. 1:30pm is 13:30
	*/
	ENTERTIME="%filltext:name=Hour:width=2%:%filltext:name=Minute:width=2%"
	
	timezones=( "America/Los_Angeles" "America/Chicago" "Europe/Dublin" )
	
	for zone in ${timezones[@]}
	do
    		TZ=$zone date -jf "%H:%M %z" "$ENTERTIME $(date "+%z")" "+%H:%M %Z";
	done




