Title: Back up Your Contacts with Pythonista
Date: 2014-09-28
Category: Tech
Tags: scripting, Dropbox, ifttt, launchcenterpro, ios, pythonista
Author: Ryan M

While it hasn't happened in a while, I have lost or had issues with contacts in iCloud. I haven't found a reliable way to automatically back up my contacts on my Mac, but Pythonista offers a simple way to back them up.

<!-- PELICAN_END_SUMMARY -->

Pythonista offers a great library which gives you access to your contacts on iOS. With a short script, I can back up my contacts to a folder in my Dropbox account. This will add a vCard file to my Dropbox account with the date the script was run.

_Note: You'll need the Dropbox login script for this to work. Visit [this][dropboxlogin] link to get it set up. I keep mine in a folder called "lib" in Pythonista._

[dropboxlogin]: https://gist.github.com/omz/4034526

You can download my Contacts Back up script [here][download].

[download]: https://gist.github.com/rjames86/79f857f427599f6e145c

{! backup_contacts.py !}

If you're like me, you're going to forget to do this on a regular basis. I hadn't yet found a reason to use the IFTTT Launch Center Pro triggers, but this turned about to be a great reason to use it. I have a trigger that goes off on the first of every month that will launch the back up script.

If you want to get reminders to back up your contacts using IFTTT, you can use the recipe below.

<a href="https://ifttt.com/view_embed_recipe/206885-backup-contacts-with-lcp" target = "_blank" class="embed_recipe embed_recipe-l_24" id= "embed_recipe-206885"><img src= 'https://ifttt.com/recipe_embed_img/206885' alt="IFTTT Recipe: Backup Contacts with LCP connects date-time to launch-center" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script>
