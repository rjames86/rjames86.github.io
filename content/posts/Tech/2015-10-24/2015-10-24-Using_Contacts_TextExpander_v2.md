Title: Using Contacts.app with TextExpander v2: Objective-C and JavaScript
Date: 2015-10-24 02:12
Category: Tech
Tags: scripting, textexpander, efficiency, javascript, objectivec
Author: Ryan M


<!-- PELICAN_BEGIN_SUMMARY --> 
I was generally happy with how I was using [Contacts.app with TextExpander][previous post] to create snippets for my emails, phone numbers and addresses. However, as I eventually realized, I have to have Contacts.app running for it to work. When AppleScript and JavaScript talk to applications in OS X, they have to be running. That isn't the case for C and Objective-C libraries, so I decided to see how hard it was to use the Objective-C bindings for Javascript.
<!-- PELICAN_END_SUMMARY --> 

The documentation is just as sparse in [the developer documentation][dev docs], however [this article][article] by Tyler Gaw helped get me started in understanding how to represent Objective-C methods in Javascript. It's probably easiest to just show the script and explain what's going on.


	:::javascript
    ObjC.import("AddressBook");
    sAB = $.ABAddressBook.sharedAddressBook
    meRecord = sAB.me

    var propertyToObjCType = {
        'email': $.kABEmailProperty,
        'address': $.kABAddressProperty,
        'phone': $.kABPhoneProperty
    }

    var labelToObjCType = {
        'work': $.kABWorkLabel,
        'home': $.kABHomeLabel,
        'iPhone': $.kABPhoneiPhoneLabel,
    }

    function valueForProperty(property){
        return meRecord.valueForProperty(propertyToObjCType[property])
    }

    function getEmailByLabel(inputLabel){
        emails = valueForProperty('email')
        label = labelToObjCType[inputLabel]
        for (var i = 0; i < emails.count; i++){
            if ($.CFEqual(emails.labelAtIndex(i), label)){
                return emails.valueAtIndex(i)
            }
        }

    }

    function getAddressByLabel(inputLabel){
        addresses = valueForProperty('address')
        label = labelToObjCType[inputLabel]
        for (var i = 0; i < addresses.count; i++){
            if ($.CFEqual(addresses.labelAtIndex(i), label)){
                return sAB.formattedAddressFromDictionary(addresses.valueAtIndex(i)).string
            }
        }

    }

    function getPhoneByLabel(inputLabel){
        phone = valueForProperty('phone')
        label = labelToObjCType[inputLabel]
        for (var i = 0; i < phone.count; i++){
            if ($.CFEqual(phone.labelAtIndex(i), label)){
                return phone.valueAtIndex(i)
            }
        }

    }


The biggest thing to point out is that if you have a method called in Objective-C like `[ABAddressBook sharedAddressBook];`, this gets converted to dot notation `$.ABAddressBook.sharedAddressBook`. The Obj-C bridge is always called with either `ObjC.` or `$.` followed by the method.

You can find a nice list of different properties and values for the address book [here](http://www.macdevcenter.com/pub/a/mac/2002/08/27/cocoa.html?page=2). For labels, the most common will be `$.kABHomeLabel` and `$.kABWorkLabel` for home and work respectively. If you've created a custom label (let's call it XXX), you can reference it by calling `$.kABXXXLabel`.

As with any other JavaScript snippet in TextExpander, you can call any of these functions to expand the contact information that you'd like.

	:::javascript
	getEmailByLabel('home')  // returns your home phone number
	
	getAddressByLabel('work')  // returns your work address
	
	getAddressByLabel('iPhone')  // returns your phone number labeled iPhone

For those of you who don't like copy/pasting the same code over and over, there's a nice little hack that you can do in TextExpander.

First, create a new Plain Text snippet with the code from the top of the post. I called the snippet "getInfoFromContacts". Once that's done, you can create new snippets that take advantage of this code by creating new JavaScript snippets with the following:

	:::javascript
	%snippet:getInfoFromContacts%
	getEmailByLabel('home')

This way, if you update something from the main part of the code, you don't have to update all of your TextExpanders.

[previous post]: {static}../2015-08-23/2015-08-23_Using-Contacts.app-with-TextExpander.md
[dev docs]: https://developer.apple.com/library/mac/releasenotes/InterapplicationCommunication/RN-JavaScriptForAutomation/Articles/OSX10-10.html#//apple_ref/doc/uid/TP40014508-CH109-SW1
[article]: http://tylergaw.com/articles/building-osx-apps-with-js
