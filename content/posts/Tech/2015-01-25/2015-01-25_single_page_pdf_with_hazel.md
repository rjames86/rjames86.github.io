Title: Save First Page of PDF for Expenses with Hazel
Date: 2015-01-25 12:46
Category: Tech
Tags: scripting, hazel, applescript, efficiency
Author: Ryan M

Once a month I have to submit my Verizon bill as an expense. The process of getting the PDF of the bill and then modifying it turned out to be a big pain by first reminding my mom to send the bill[^1], saving the first page and then submitting it for reimbursement. Turns out that Hazel can take care of everything beyond the actual submission.
<!-- PELICAN_END_SUMMARY -->  
I'm fine with reminding my mom to put the PDF in Dropbox, but I then have to check back every-so-often to see if she's actually done it. I've created a rule now that will check for any files in our shared Verizon Bill folder and if Hazel hasn't seen it before, it will send me a push notification with Pushover.

![pushover_hazel_verizon]({static}pushover_hazel_verizon.png)

I then wrote a handy little Applescript based on PDFPenPro's default script called Split PDFs that will take the first page of a PDF and save it to a new file. I differentiate the files by just adding "SINGLE PAGE" to the filename

	:::applescript
	set basePath to "/path/to/verizon/folder"

	tell application "PDFpenPro"
		open theFile as alias
		set originalDoc to document 1
		set docName to name of originalDoc
		
		if docName ends with ".pdf" then
			set docNameLength to (length of docName)
			set docName to (characters 1 thru (docNameLength - 4) of docName as string)
		end if
		
		
		set newDoc to make new document
		set savePath to ((basePath as rich text) & docName & " SINGLE PAGE" & ".pdf")
		
		copy page 1 of originalDoc to end of pages of newDoc
		
		save newDoc in POSIX file savePath
		
		quit
	end tell

Finally, so that I don't forget to submit the expense, I have one final Applescript that creates a todo item in Omnifocus based on David Spark's post [here][sparks]

	:::applescript

	set theDate to current date
	set deferDate to (current date)
	set dueDate to (current date) + (1 * days)
	set theTask to "Expense Verizon Bill"
	set theNote to theFile
	
	tell application "OmniFocus"
		tell front document
			set theContext to first flattened context where its name = "A Context"
			set theProject to first flattened project where its name = "Expenses"
			tell theProject to make new task with properties {name:theTask, note:theNote, context:theContext, defer date:deferDate, due date:dueDate}
		end tell
	end tell



[sparks]: http://macsparky.com/blog/2012/8/applescript-omnifocus-tasks
[^1]: We're on a family plan

