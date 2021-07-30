Title: Backup Your Contacts v2 : Yosemite’s Javascript Automation
Date: 2014-12-14
Category: Tech
Tags: scripting, applescript, javascript
Author: Ryan M

I recently read MacStories' [article][macstories] and was curious how easy this was to learn. Applescript never made sense to me and I spent more time trying to piece together examples than actually writing anything meaningful. I don't trust iCloud to keep my contacts safe, and I'm still using [my previous workflow][previous_workflow] with [Launch Center Pro][lcp] and [Pythonista][pythonista] to back up my contacts.
<!-- PELICAN_END_SUMMARY -->  
My first attempt at the new JSX Automation was a script to back up my contacts, which would allow me to run this automatically on my Mac Mini server. Here is what the script looks like

	:::javascript
	var app = Application.currentApplication()
	app.includeStandardAdditions = true

	now = new Date()
	nowString = now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate()

	// Replace outputFile with this if you want to automatically set the path
	// var outputFile = Path('pick your path')	
	var outputFile = app.chooseFileName({
		withPrompt: "Pick where to save your vCard backup.",
		defaultName: nowString + "_backup.vcf"
	})

	var a = app.openForAccess(outputFile, {writePermission: true})
	Contacts = Application('/Applications/Contacts.app')
	contacts = Contacts.people()
	outputString = ''

	for (var i = 0; i < contacts.length; i++){
	  outputString += contacts[i].vcard()
	}

	app.write(outputString,{
		to: a,
		startingAt: 0,
		as:'text'
	})
	app.closeAccess(outputFile)
	
	app.displayNotification("Backup finished!",{
		withTitle: "Backup Contacts",
		subtitle: contacts.length + " contacts backed up."
	})

The current script lets you choose the path to save the file. You can change this to have it be the same path every time if you want (see the instructions in the comments above).

You can download the script [here][download] to try it for yourself.

Big thank you to Alex Guyot at MacStories for his introduction to Javascript Automation.

[download]: {attach}BackupContacts.zip
[macstories]: http://www.macstories.net/tutorials/getting-started-with-javascript-for-automation-on-yosemite/
[lcp]: http://contrast.co/launch-center-pro/
[pythonista]: http://omz-software.com/pythonista/
[previous_workflow]: {static}../2014-09-28/2014-09-25_backup_contacts_with_pythonista.md
