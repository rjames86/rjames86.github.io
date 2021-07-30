Title: Clearing Multiple Notifications in Mac OS X
Date: 2016-04-18 20:04:59
Modified: 2016-12-04
Category: Tech
Tags: scripting, keyboardmaestro, alfred, efficiency, javascript
Author: Ryan M

If I haven't used my computer for a while, I'll end up with multiple calendar notifications that I have to painfully close one by one. I went searching for something that would let me close them faster, but nothing I could find did quite what I wanted.

Nearly every day I come home from work to a slew of notifications from my day.

![notifications]({static}notifications.png)

One way to close all these is to open up the Notification Center panel and click all of the X's, which will also clear out your notifications. That's still janky and I'd rather have this done without having to click a bunch of times.

I first wrote the script using Applescript. I ran into some annoying issues when trying to ignore certain notification windows, such as System Updates. I wanted to ignore that window entirely, and since Applescript doesn't have a `continue` in for-loops I opted to use Javascript which ended up being easier.

	:::javascript
	var app = Application("System Events")

	notificationCenter = app.processes.byName('NotificationCenter')

	function closeWindow(window){
	    window.buttons.whose({
	        _or: [
	            {name: "Close"},
	            {name: "OK"}
	        ]
	    })().forEach(function(button){button.click()})
	    delay(0.1); // The UI can't always keep up, so we introduce a short delay
	}

	notificationCenter.windows().forEach(closeWindow)

I'm currently running this in Keyboard Maestro, but it could just as easily be run with Alfred. I've made very basic versions using both for download:

- [Alfred][alfred]
- [Keyboard Maestro][km]


[alfred]: {static}/downloads/ClearNotificationsAlfred.zip
[km]: {static}/downloads/ClearNotificationCenterKM.zip
