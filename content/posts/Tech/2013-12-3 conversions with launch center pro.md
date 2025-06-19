Title: Quick Conversions with Launch Center Pro and Soulver
Date: 2013-12-03
Category: Tech
Tags: ios, automation, automation
Author: Ryan M

There are some great tools out there to convert things like currency, distances and measurements. Even Siri can do this fairly well, but the one thing I always find frustrating is that the process of doing this can be fairly slow and in a lot of cases requires a data connection. Growing up in the United States, I was unfortunately never exposed to the metric system or Celsius. Since I've moved to Dublin, I'm find myself doing a lot of conversions from one unit to another.
<!-- PELICAN_END_SUMMARY -->  

I was poking around in [Launch Center Pro][lcp] for iOS the other day to just see what kinds of things I could do, and I noticed one of the options was [Soulver][soulver]. My main use case for Soulver has always been one-off conversions or keeping score while playing Farkle with my girlfriend. It occurred to me that this would make a really nice way to do quick conversions. 

I didn't want to have to create a mess of different actions for each unit. The way around this was to create a variable within Soulver and always reference back to it with multiple conversions. I started out simple with a quick US Dollar to Euro and Pounds and vice-versa. 

![Currency Conversion]( {static}/assets/articles/conversions-launch-center-pro/lcp_currency.jpg)

To achieve this, Launch Center Pro uses x-callback-urls which allows apps to send data to another app and perform actions. The following url requests a number and then sends over this number as a variable to Soulver

{! /assets/articles/conversions-launch-center-pro/soulver.txt !}
    
This worked perfectly and solved the two biggest requirements that I had: to be quick and to not rely on a data connection. I then wanted to go a little further and so I did some very basic unit conversions.

![Unit Conversions]( {static}/assets/articles/conversions-launch-center-pro/lcp_temp.jpg)  

The url for the action is very similar, but using different conversions

	:::html
    soulver://new?text=x%20%3D%20[prompt-num:Text]%0AFahrenheit%3A%20x%20C%20to%20F%0ACelsius%3A%20x%20F%20to%20C%0A-%20-%20-%20-%20-%20-%20-%20-%20-%20-%20-%20-%20%0AMiles%3A%20x%20km%20to%20mi%0AKilometers%3A%20x%20mi%20to%20km%0A-%20-%20-%20-%20-%20-%20-%20-%20-%20-%20-%20-%20%0AFeet%3A%20x%20m%20to%20feet%0AMeters%3A%20x%20feet%20to%20m%0A----------------&title=Temperature  

If you have both Launch Center Pro and Soulver, you can download both of these actions here:

[Currency Conversion][currency]  
[Unit Conversions][unit]  

[lcp]: http://contrast.co/launch-center-pro/
[soulver]: http://www.acqualia.com/soulver/iphone/
[currency]: http://launchcenterpro.com/2xv247
[unit]: http://launchcenterpro.com/ylljt1
