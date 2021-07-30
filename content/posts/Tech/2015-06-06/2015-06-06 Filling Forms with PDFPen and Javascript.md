Title: Filling Forms with PDFPen and Javascript
Date: 2015-06-06 04:15
Category: Tech
Tags:  scripting, efficiency, javascript, applescript
Author: Ryan M

My adventure with Mac Javascript Automation continues. Things still aren't easy and the documentation is poor, but I'm finding that it's still easier to write automation scripts in Javascript than it ever was with Applescript.
<!-- PELICAN_END_SUMMARY -->  
Every month I need to fill out four receipts in a PDF form that I made with PDFPenPro. I never liked doing it and I felt like there had to be a way to do this better. I did some searching, and of course came across an [old post](http://leancrew.com/all-this/2012/02/automatic-w-9s-with-pdfpen) by Dr. Drang where he was adding rich text to PDFs. This was close to what I wanted, but since I had taken the time to create the form fields myself, I figured I should take advantage of them if I could.

After some painful reading of the PDFPen Javascript library and playing around, I found that I was able to set the values of form fields if they had assigned names. I first went through the process of naming all of my form fields.

![formnames]({static}formnames.png)

First we start with creating our app variable for PDFPen

	:::javascript
	app = Application("PdfPenPro")
	app.includeStandardAdditions = true;

After that, I created a few functions to easily set the values for text fields and buttons

	:::javascript
	function getFormField(doc, field) {
	    formField = doc.pages()[0].imprints.whose({fieldName: field})()
	                    
	    if (formField.length) {
	        return formField[0]
	    }
	    return
	}
	
	function setFormField(doc, field, value) {
	    theField = getFormField(doc, field)
		if (theField.class() == "button") {
			theField.checked = value
		} else {
		    theField.value = value
		}
	}

I've found that with PDFPen (or maybe more generally), keeping track of windows in applications with Javascript can get tricky. The order in which they appear can change, and so I've written myself a few helper functions to keep track of documents as I work through scripts.

	:::javascript
	var getByName = function(fileName){
	    return app.documents.byName(fileName);
	}
	var getDocPage = function(fileName, pageNum) {
	    return getByName(fileName).pages[pageNum-1];
	}

These are helpful when I want to duplicate my template receipt that I've created and not run the risk of overwriting the original.

	:::javascript
	function createNewReceipt() { 
	    /*
	        Opens the Receipt template
	        Creates a new document and duplicates
	        the template into the new doc
	    */
	    app.open(templatePath)
	    var currentDoc = app.windows[0].document
	    var currentDocName = currentDoc.name()
	    doc = app.Document().make()
	    app.duplicate(getDocPage(currentDocName, 1), {to:doc})
	    return doc
	}

At this point, it's simply a matter of filling in the fields however[^1] I like. I chose to have a few input fields and optional lists. Here are examples of both of those and how they can be implemented in Javascript.

	:::javascript
	/*
		Creates a list to choose from where the options
		are an array called dateOptions.
		I always take the 0 element since I don't allow
		empty selections and multiples aren't allowed
	*/
	dateChoice = app.chooseFromList(
	                        dateOptions,
	                        {withTitle: "Start Date",
	                        withPrompt: "Choose Start Date", 
	                        defaultItems: dateOptions[1],
	                        multipleSelectionsAllowed: false,
	                        emptySelectionAllowed: false}
	            )[0]

	/* 
		Basic dialog box. 
		defaultAnswer has to exist, otherwise there
		won't be a text box to type into
	*/
	receivedFrom = app.displayDialog("Who sent the check?", {defaultAnswer: ""})

I then created an array of all the fields that I wanted to be filled.

	:::javascript
	fieldsToFill = [
    { value: receivedFrom.textReturned, fieldName: "ReceivedFrom" },
    	...
    { value: paymentType == "Check" ? true : false, fieldName: "CheckCheckBox" }
    ]

The very last lines are where the magic happens and all the fields are filled out. It was pretty fun to watch the form fill almost instantly and then let me save it.

	:::javascript
	newDoc = createNewReceipt()
	fieldsToFill.map(function(obj){setFormField(newDoc, obj.fieldName, obj.value)})

	saveLocation = app.chooseFileName({defaultName: rentReceiptName(dateChoice), defaultLocation: savePath})
	newDoc.save({in: saveLocation})

That's it! This will take a lot of the slow process out of filling out my receipts each month. The next step will probably be generating the email and attaching the PDF. PDFPen already includes a script to do this very thing, so no more work needed for me. You can see the entire script [here][gist]

[gist]: https://gist.github.com/rjames86/8ee61652087a2c44802f

[^1]: I found [this resource](https://github.com/dtinth/JXA-Cookbook/wiki/User-Interactions) helpful to get me started on user input interactions

