Title: Searching Todo’s in Code
Date: 2016-01-11 08:55
Category: Tech
Tags: scripting, efficiency, bash, sublimetext
Author: Ryan M

Happy 2016! It's been a while since I've gotten something up here.
<!-- PELICAN_BEGIN_SUMMARY -->
Last week at work I was working on a fairly large refactor of our front-end. Large pieces of code were being moved around and others re-written to be cleaner and more understandable. Throughout this process, I was leaving myself todo's so that I'd remember to fix something later.  Problem is, I would rarely ever go back to them. That was until someone on my team shared some bash functions they had written to make following up on those todo's much easier
<!-- PELICAN_END_SUMMARY -->

It's fairly common practice to leave yourself todo's as comments in code such as

	# TODO(ryan) fix this later.

That way if someone comes across it in the future, they'll know that whatever is below may not be perfect and that I plan on fixing it at some point. Finding all your todo's later is a different story. That's where some fancy bash functions come in handy.

	:::bash
    function ga_code_search() {
        # alias todo='ga_code_search "TODO\(`whoami`\)"'
        SCREEN_WIDTH=`stty size | awk '{print $2}'`
        SCREEN_WIDTH=$((SCREEN_WIDTH-4))
        # Given a spooky name so you can alias to whatever you want. 
        # (cs for codesearch)
        # AG is WAY faster but requires a binary 
        # (try brew install the_silver_searcher)
        AG_SEARCH='ag "$1" | sort -k1 | cat -n | cut -c 1-$SCREEN_WIDTH'

        # egrep is installed everywhere and is the default.
        GREP_SEARCH='egrep -nR "$1" * | sort -k1 | cat -n | cut -c 1-$SCREEN_WIDTH'

        SEARCH=$AG_SEARCH

        if [ $# -eq 0 ]; then

            echo "Usage: ga_code_search <search> <index_to_edit>"
            echo ""
            echo "Examples:"
            echo "    ga_code_search TODO"
            echo "    ga_code_search TODO 1"
            echo "    ga_code_search \"TODO\\(graham\\)\""
            echo "    ga_code_search \"TODO\\(graham\\)\" 4"
            echo ""        
            return
        fi
        
        if [ $# -eq 1 ]; then
            # There are no command line argumnets.
            eval $SEARCH
        else
            # arg one should be a line from the output of above.
            LINE="$SEARCH | sed '$2q;d' | awk -F':' '{print +\$2 \" \" \$1}' | awk -F' ' '{print \$1 \" \" \$3}'"
            # Modify with your editor here.
            emacs \+`eval $LINE`
        fi    
    }


If you read through the comments, `the_silver_searcher` is far faster than `grep` for searching contents of files. If you don't have it already, I'd highly suggest installing it with `brew install the_silver_searcher`. If you don't want to, be sure to change `SEARCH=$AG_SEARCH` to `SEARCH=$GREP_SEARCH`.

The function itself isn't that interesting. It's when you assign aliases to use this function that things become interesting. Here are the three that were given to me:

	:::bash
	# Find todo items that are assigned to me. TODO(ryan)
	# You can change `whoami` to whatever you want.
	alias todo='ga_code_search "TODO\(`whoami`\)"'

	# Find merge conflicts that need to be resolved.
	alias conflicts='ga_code_search "<<<<<<<<<"'

	# Find anything below your CWD.
	# You can now type `cs some_piece_of_code`
	alias cs='ga_code_search'

My favorite by far is the first alias `todo`. Here is some example output when running this command:


	:::bash
    > my_project (master): todo
     1	app/models/strava.py:102: # TODO(ryan) probably should memoize this at some point so its faster.
     2	app/models/strava.py:148: # TODO(ryan) make this line prettier
     3	app/templates/strava/index.html:50: <!-- TODO(ryan) move this into its own template file at some point -->



Notice how there are numbers next to each result? That's because you can also open the file right to that todo item by typing `todo 1`! As the function is written, it will open in emacs. If that's your editor of choice, you'll be set. I'm personally a fan of Sublime Text. There's a way to also open a file in Sublime Text to a specific line number. Simply change the text in red with that in green:


	:::diff
	- LINE="$SEARCH | sed '$2q;d' | awk -F':' '{print +\$2 \" \" \$1}' | awk -F' ' '{print \$1 \" \" \$3}'"
	+ LINE="$SEARCH | sed '$2q;d' | awk -F':' '{print +\$2 \" \" \$1}' | awk -F' ' '{print \$3 \":\" \$1}'"

	- emacs \+`eval $LINE`
	+ subl `eval $LINE`

I've only used the functions for a few days now, but it's greatly improved my workflow for getting old todo's done in code. If you'd like to download these scripts, [here](https://gist.github.com/2819e0576e9280a985ae) is the Sublime Text version and the [emacs](https://gist.github.com/1351952bdc55d206d939) version.
