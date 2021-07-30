Title: Automatically Attach tmux in SSH Session
Date: 2015-05-09 09:47
Category: Tech
Tags: scripting, efficiency, bash
Author: Ryan M

I frequently work in ssh sessions and have found terminal multiplexers like `tmux` to be invaluable. The problem I was constantly facing was having to re-attach or create a new  session each time I would ssh into a machine. Sometimes I would accidentally create a new session when one already existed and would then have to find where I had been working previously.
<!-- PELICAN_END_SUMMARY -->  

After searching around, I found a nice way to automatically create a  session each time I ssh into a machine, or re-attach if it already exists.

	:::bash
    if [[ "$TMUX" == "" ]] &&
            [[ "$SSH_CONNECTION" != "" ]]; then
        # Attempt to discover a detached session and attach
        # it, else create a new session
        WHOAMI=$(whoami)
        if tmux has-session -t $WHOAMI 2>/dev/null; then
    	tmux -2 attach-session -t $WHOAMI
        else
            tmux -2 new-session -s $WHOAMI
        fi
    fi

I first check to be sure I'm not in a `screen` session and also that I'm using ssh and not local to my machine. After that, it's a simple check to see if a  session exists. If so, re-attach it, otherwise create a new one. This can be simple added to the bottom of your ~/.bashrc file. Now every time I ssh in to any machine, my previous session is sitting there waiting for me.

![tmux]({static}tmux.gif)
