Title: Setting Keyboard Shortcuts from Terminal in macOS
Date: 2017-01-05 08:54
Tags: automation, bash
Author: Ryan M

It's been a few months since my last post. I've spent a lot of time working on my blog, but all things behind the scenes that most people wouldn't even notice. 

Setting keyboard shortcuts on Mac is actually fairly easy, but it requires a lot of clicking around. Fortunately there's a way to do this from the terminal that's faster and easier.
<!-- PELICAN_END_SUMMARY -->

The `defaults` command in MacOS is nothing short of a mystery. It does some powerful things, but the documentation is sparse and half of the time I don't know what I'm doing. That being said, I've had a script written for a long time called `new_computer.sh` where I set all of my favorite global and application-specific shortcuts when getting a new computer.

Let's take an example of a shortcut everyone should have: Print As PDF from within a print dialog. I've always set it to ⌘ ⇧ P. To do this within System Preferences, the steps are:

1. Open the Keyboard preference Pane
2. Click the Shortcuts tab
3. Click App Shortcuts
4. Click the + symbol
5. Fill out the prompts
    - Leave All Applications Selected
    - Menu Title is "Save as PDF…" (it's an elipsis, not three periods. Type `option ;` to get the symbol)
    - Choose your shortcut

It's almost too many steps for one shortcut, let alone multiple. Let's try this in Terminal:

    :::bash
    defaults write -globalDomain NSUserKeyEquivalents  -dict-add "Save as PDF\\U2026" "@\$p";

Easy, right? Sort of. The syntax for writing global shortcuts is fairly straight forward. If you're not creating a shortcut for a specific application, you can use the command above and simply change the title and shortcut. Here are how to represent all of the modifier keys:

- @ is command
- ^ is control
- ~ is option
- $ is shift

So command-shift p becomes `"@\$p"`.

The reason this came up was that Omnifocus recently added tabs. This is great except that there's no shortcut for cycling through the tabs. This makes the feature almost pointless for me. So to add shortcuts, I ended up using the command above, but I need to target Omnifocus only.


    :::bash
    defaults write com.omnigroup.OmniFocus2 NSUserKeyEquivalents -dict-add "Show Next Tab" "^\\U005D"
    defaults write com.omnigroup.OmniFocus2 NSUserKeyEquivalents -dict-add "Show Previous Tab" "^\\U005B"

Here I'm setting show next/previous tab to control [ and control ]. Once you've set your keyboard shortcuts, you'll need to quit and re-launch the application in order for the new preferences to be read.
