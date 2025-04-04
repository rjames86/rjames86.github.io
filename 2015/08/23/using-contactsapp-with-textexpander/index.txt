Title: Using Contacts.app with TextExpander
Date: 2015-08-23 11:41
Modified: 2015-09-20 14:08
Category: Tech
Tags: textexpander, automation, javascript
Author: Ryan M

Changing your email or phone number isn't fun. You have to tell everyone, update all of your online accounts, and make sure your TextExpanders are up-to-date with the right information. One of the places I will always update is my contact information in Contacts.app, so why not just use that as the source of truth for TextExpander snippets?
<!-- PELICAN_END_SUMMARY --> 

In TextExpander 5, you can now use Javascript in snippets. Since I had [already created some scripts][Backup Contacts] using Contacts, I re-used some of the bits to create TextExpander snippets to expand information directly from Contacts.app.

	:::javascript
    Contacts = Application('/Applications/Contacts.app')

	// ::attr is the attribute you want pull (emails, phones, etc.)
	// ::accountType is what you see to the left of the info in Contacts.app
    function getMyInfo(attr, accountType){
        method = attr == 'addresses' ? 'formattedAddress' : 'value'
        search = Contacts.myCard()[attr].where({label: accountType})
        results = search.length ? search().map(function(a){return a[method]()}) : []

        if (results.length == 1){
            return results[0]
        } else if (results.length > 1){
            return results.join(", ")
        } else return ""
        
    }

    // Grab my 'blog' email address 
    getMyInfo('emails', 'blog') // returns email address

The `getMyInfo` function is fairly generalized to allow you to get any basic information like emails or phone numbers from your contacts. The first argument is the type[^1], and the second is the label you want, such as Home, Work, etc. To get a phone number, just change the function called to `getMyInfo('phones', 'iPhone)`. To get an address, change to `getMyInfo('addresses', 'home')`, which will return a formatted address.

*Update 2015-08-23*: Updated the `getMyInfo` function to support addresses.  

*Update 2015-09-20*: For a while, I couldn't figure out why occasionally expanding things from Contacts would take a little while. Then I realized, for AppleScript to work, the application you're calling needs to be open. If you do want to use this as a way to expand your information from Contacts, just know that you'll need to be running the application for the TextExpander snippets to work.

*Update 2015-09-20*: I've figured out a way to do this without Contacts.app running! Check out my post [here]({static}../2015-10-24/2015-10-24-Using_Contacts_TextExpander_v2.md) for more info.


[Backup Contacts]: {static}../2014-12-14/2014-12-14_backup-your-contacts-v2.md
[^1]: You can find all the attributes in the Contacts.app scripts library in Address Book Script Suite → Application → myCard
