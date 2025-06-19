Title: Writing Notes with Alfred 2
Date: 2013-05-14
Category: Tech
Slug: notes_and_alfred
Tags: alfred, automation
Author: Ryan M

I started coding about two years ago and only recently discovered the wonders of Markdown.  Every time I'd learn something new, I would keep it in a text file with TextEdit. This was good and fine until a coworker introduced me to Notational Velocity. This completely changed the way I managed my notes but I always felt like I was missing something. That's when I discovered NVAlt. It let me keep the simplicity of plain text but format the note with the wonders of Markdown. 
<!-- PELICAN_END_SUMMARY -->  

Now I was left with another problem. I was annoyed having to command-tab over to NVAlt, command-D to go to the search field and type just to find the note. With Alfred 2's new File Filter, I can now search specifically for my notes within Alfred. I now just launch Alfred, type 'note' and any keywords I want and am immediately taken to my note in NVAlt. 

![alfred_note]( {static}/assets/articles/notes-and-alfred/alfred_note.png )

This last week I've spent a lot of time writing up plans and documents. I wouldn't put NVAlt in the category of great text editors and so I've been using MultiMarkdown Composer, but I'm still saving to the same notes folder. It seemed only obvious to add more functionality to my Alfred script. Now I can optionally hold down command or control to open my note in MultiMarkdown Composer or Byword respectively. 

![open_in_mmc]( {static}/assets/articles/notes-and-alfred/open_in_mmc.png )

You can download the Alfred Extension here:

[![image]( {static}/images/alfred_extension.jpg )][download_url]  

Be sure to set your path to your notes folder in the File Filter under Search Scope. If you're using Notational Velocity, you can change which application is opened in the action script. 

[download_url]: {static}/assets/articles/notes-and-alfred/Notes.alfredworkflow
