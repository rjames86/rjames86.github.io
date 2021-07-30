Title: Backup Your Email with Getmail
Date: 2015-09-06 06:45
Category: Tech
Tags: scripting, email, backup
Author: Ryan M

It's always a good idea to keep backups of data you can't replace, including email. For the last few years, I've had a script that automatically backs up my Gmail account. Since switching to Fastmail, I figured I should continue doing the same thing. It turned out, it was pretty easy to set up another account.

<!-- PELICAN_END_SUMMARY -->  

I've been meaning to write about backing up email for a few months now. With Dr. Drang's [recent post][drangs post] about archiving email using `formail`, I figured this a good enough time as ever to post my solution.

To install `getmail`, you can use Homebrew, or [manually][manual install] if you're in to that sort of thing.

	brew install getmail

For the configuration files, I first created a directory in my Home folder

	mkdir .getmail

The config files for both Fastmail and Gmail are similar, but I'll include both for completeness

#### Gmail

    [retriever]
    type = SimpleIMAPSSLRetriever
    server = imap.gmail.com
    username = <username>@gmail.com
    mailboxes = ("[Gmail]/All Mail",) # To pull all emails
    port = 993

    [destination]
    type = Maildir
    path = ~/gmail-archive/

    [options]
    # print messages about each action (verbose = 2)
    # Other options:
    # 0 prints only warnings and errors
    # 1 prints messages about retrieving and deleting messages only
    verbose = 2
    message_log = ~/Dropbox/Scripts/logs/gmail.log
    receieved = false
    delivered_to = false
    # dont re-read messages its already pulled down
    read_all = false

#### Fastmail ####

    [retriever]
    type = SimpleIMAPSSLRetriever
    server = mail.messagingengine.com
    username = <username>@fastmail.com
    mailboxes = ("INBOX.Archive",)

    [destination]
    type = Maildir
    path = ~/fastmail-archive/

    [options]
    verbose = 2
    read_all = false
    message_log = ~/Dropbox/Scripts/logs/fastmail.log
    delivered_to = false
    received = false

You'll notice that I don't include the password in either config. If password is omitted from a config on Mac OS, the first time you run `getmail`, you'll be prompted to enter your password and it will then be stored securely in KeyChain. Since I'm using Maildir as my type, you'll need to create special folders, with 3 specific subfolders

	:::bash
	mkdir ~/fastmail-archive
	mkdir !$/{cur,tmp,new} # creates 3 new folders in ~/fastmail-archive

The same will need to be done for ~/gmail-archive.

Once this is set up, you'll need to run the script once to enter in your password

	/usr/local/bin/getmail -q -r ~/.getmail/getmail.gmail

If I ever need to view the emails, I do the same as Dr. Drang and use `mutt`, which can also be installed with Homebrew.

	mutt -R -f ~/gmail-archive

[drangs post]: http://leancrew.com/all-this/2015/09/archiving-old-mail-with-formail/
[manual install]: http://pyropus.ca/software/getmail/documentation.html#installing
