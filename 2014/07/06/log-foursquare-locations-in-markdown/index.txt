Title: Log Foursquare Locations in Markdown
Date: 2014-07-06
Category: Tech
Tags: markdown, automation, bash, ifttt
Author: Ryan M

I've always used Foursquare as a way to remember the places I had visited while traveling. Foursquare isn't really meant to be used in this way, and as a result, they don't make it easy to answer the question, "what was that restaurant I went to last time I was here?" I'm now using IFTTT to log all my checkins to a text file in my Dropbox account.
<!-- PELICAN_END_SUMMARY -->  

I like MultiMarkdown tables. So that my Foursquare checkins looked nice, I first created a file in my Dropbox account with a heading

	:::markdown
	| Date |  VenueName  | VenueUrl | Shout | MapURL |  City | State | Country |
	| :---: | :---: | :---: | :---: | :---: | :---: |

In IFTTT, I then created a recipe which matches my table headers

[iftttrecipe]: https://ifttt.com/recipes/187719-share-foursquare-checkins-in-amarkdown-table "Share Foursquare checkins in amarkdown table by rjames86 - IFTTT"

<center><a href="https://ifttt.com/view_embed_recipe/187719-share-foursquare-checkins-in-mamarkdown-table" target = "_blank" class="embed_recipe embed_recipe-l_45" id= "embed_recipe-187719"><img src= 'https://ifttt.com/recipe_embed_img/187719' alt="IFTTT Recipe: Share Foursquare checkins in mamarkdown table connects foursquare to dropbox" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script></center>

![IFTTT Content]( {attach}content.png )

You may have noticed that I added an additional "Address" column that isn't getting filled out. IFTTT doesn't explicitly give the address of the venue you visited. However, the link to the Google Maps image contains GPS coordinates that I can use. Dr. Drang's [post][drdrang] gave me the idea to parse out the coordinates and then use them how I'd like. This script, which I'm using with Hazel each time the file is updated, reverse geolocates the coordinates and returns the full address using OpenStreetMap. After that, it appends that address to each line in the markdown file.

[drdrang]: http://www.leancrew.com/all-this/2014/07/extracting-coordinates-from-apple-maps/ "Extracting coordinates from Apple Maps - All this"

{! extract.sh !}

In the end, the table then ends up looking something like this:

| Date |  VenueName  | VenueUrl | Shout | MapURL |  City | State | Country |
| :---: | :---: | :---: | :---: | :---: | :---: |  :---: |  :---: |
| July 06, 2014 at 07:07PM | Third Floor Espresso (3FE) | http://4sq.com/rtEJWP |  | [Map Link](http://maps.google.com/maps/api/staticmap?center=53.33998,-6.242084&zoom=16&size=710x440&maptype=roadmap&sensor=false&markers=color:red%7C53.33998,-6.242084) | Dublin |  | Republic of Ireland |  
| July 06, 2013 at 10:00AM | Wooly Pig Cafe | http://4sq.com/1n5Scct  | | [Map Link](http://maps.google.com/maps/api/staticmap?center=37.76522,-122.460266&zoom=16&size=710x440&maptype=roadmap&sensor=false&markers=color:red%7C53.33842395309077,-6.234097712535167) |  San Francisco | California | United States of America |
