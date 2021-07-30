Title: List Server Favorites in OS X 10.11 El Capitan
Date: 2015-10-31 02:11
Category: Tech
Tags: scripting, efficiency, javascript, objectivec
Author: Ryan M

I'm using Alfred a lot less these days. Many of my workflows have been easier to build in Keyboard Maestro. The remaining few that are left in Alfred are ones that I heavily depend on, one of which is accessing my Server Favorites in OS X. 

Up until OS X 10.11 El Capitan, Server Favorites were stored in a plist file called `com.apple.sidebarlists.plist`. I finally got around to upgrading my computers at home only to realize that my "server" workflow stopped working. After inspecting the plist file, I found that those favorites were gone and were hiding elsewhere. After a bunch of searching, and the help of Houdaspot, I found them in `~/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.FavoriteServers.sfl`. What is this `sfl` extension? Still not really sure, but after some poking around, [this](https://gist.github.com/pudquick/4776b4b2075bf9b7e512) was the only resource I could find that helped me get started. 

I don't necessarily like the CoreFoundation stuff in Python, and since I'm on a OS X JavaScript automation roll right now, I decided to give it a try. Turns out, it's really easy.

	:::javascript
    items = $.NSKeyedUnarchiver.unarchiveObjectWithFile('/Users/username/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.FavoriteServers.sfl')

    items = items.objectForKey('items')
    itemsCount = items.count

    to_ret = []
    while (itemsCount--){
    	  item = items.objectAtIndex(itemsCount)
        to_ret.push(
        	{
        		name: item.name, 
        		url: item.URL.absoluteString
        	}
        )
    }

    to_ret

This returns a nice object of the name and url for the servers in your favorites.

You can download the workflow here.

[![image]( {static}/images/alfred_extension.jpg )][download_url]    



[download_url]: {static}/downloads/VNC_Favorites.alfredworkflow
