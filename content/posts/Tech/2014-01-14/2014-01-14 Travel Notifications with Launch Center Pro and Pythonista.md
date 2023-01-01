Title: Travel Notifications with Launch Center Pro and Pythonista
Date: 2014-01-14
Category: Tech
Tags: automation, pythonista
Author: Ryan M
Slug: travel-notifications

I've been doing a lot more traveling in the last year. Each time I take off or land, I found myself sending nearly the same text message to multiple people. After a while, it began to feel more like a chore than the kind gesture of letting others know I made it safely. For the repetitive messages, I found  way of automating nearly the entire process.
<!-- PELICAN_END_SUMMARY -->  

Now that Launch Center Pro has the `launchpro-messaging://` action with x-callback-url support, I can chain SMS messages together. This is something I've been wanting for a long time for this specific use case. When I began writing the action, I found one hiccup in which is I would need to write the message to each individual person unless I wanted to first copy it to my clipboard before running the action. I didn't have luck with the `launchpro-clipboard://` action while calling the clipboard from the same action even though it is supposed to work in theory[^1].

I decided to venture out and use Pythonista to generate the url scheme for me and then pass it back into Launch Center Pro's in-app messaging. The nice thing here is that I can cleanly list out all of the contacts to whom I'd like to send the message from with in the script and change the action much more quickly.
	
	:::python
	contacts = [
		'friend1@dropbox.com',
		'mom@gmail.com',
		'+1-555-867-5309'
	]

The script is written in such a way that I can put as many contacts in as I want and the url scheme will still get generated correctly with the url-escaping. 

Now, I have a nice list of message options in Launch Center Pro that will then send the same message to all of my contacts:

![Launch Center Pro notifications]({attach}lcp_notifications.png)

If the "Just Landed" option is chosen, a new prompt will be given to type in the place where I landed. Once I'm brought back into the app, I just need to hit send for each message.

<span style="text-align: center; display: block;">
<iframe src="//player.vimeo.com/video/84171813?title=0&amp;byline=0&amp;portrait=0" width="361" height="642" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
</span>


You can download the Python script [here][python] and the Launch Center Pro action can be found [here][lcp]

\[Update\] 2014-02-15  

I made some updates to the script so that you can send custom notifications for each individual person. It also uses Pythonista's location services to automatically put in the city name to make it easier.

    :::python
    contacts = [
         {
            'address': 'person1@gmail.com',
            'landed': 'Hi, Mom. Just landed in ',
            'boarding': 'Boarding now!',
            'shuttingdown': 'Shutting down. I\'ll text when I land.'
         },
         {
            'address': '+1 555 867 5309',
            'landed': 'Hi, John. Just landed in ',
            'boarding': 'Boarding now.',
            'shuttingdown': 'Shutting down. See you soon!'
         },
    ]

[Here's][python2] a link to the updated version.
[lcp]: http://launchcenterpro.com/k0p747
[python]: {attach}Travel_Notices.py
[python2]: {attach}Travel_Notices2.py

[^1]: The developers mention a workaround [here](http://help.contrast.co/hc/en-us/articles/200611883-x-callback-url-Support), but I wasn't able to get it to work.
