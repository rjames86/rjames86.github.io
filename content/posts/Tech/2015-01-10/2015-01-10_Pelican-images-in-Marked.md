Title: View Image Links from Pelican in Marked 2
Date: 2015-01-10
Category: Tech
Tags: automation, python, pelican
Author: Ryan M

I really enjoy writing in MultiMarkdown Composer and having Marked display a rendered version. When writing blog posts like this, images would never appear since Pelican's syntax for displaying images is `{static}/path/to/image`. I looked into Marked's preprocessor abilities and figured out a nice, clean way to display images when writing blog posts.
<!-- PELICAN_END_SUMMARY -->  
In Marked's preferences under Advanced, there is an option to add your own preprocessor. This gives you the ability to format the text in the file before Marked renders the markdown.

![marked_preferences]({static}marked_preferences.png)

The script simply looks for any occurrence of the `{static}` and replaces it with the path to my content folder in Pelican.

	:::python
    #!/usr/bin/python
    import sys
    import re
    import os

    home = os.path.expanduser('~')


    class PelicanFormat:
        def __init__(self):
            self.blog_path = home + '/Dropbox/blog/content'
            self.content = sys.stdin.read()

        def __repr__(self):
            return sys.stdout.write(self.__str__())

        def __str__(self):
            return self.content

        def replace_filenames(self):
            self.content = re.sub(r'{static}', self.blog_path, self.content)

        def change_codeblocks(self):
            """
            TODO Pelican uses ':::language' to override syntax highlighting.
            """
            pass

    if __name__ == '__main__':
        p = PelicanFormat()
        p.replace_filenames()
        print p


Now I can preview images for my blog posts instead of broken images.

---

*Bonus!*

This is a Text Expander snippet I use to create image urls for Pelican. It looks for the last file that was added to my images folder and then creates the url

	:::bash
    #!/bin/bash

    DROPBOX_PERSONAL=$(python -c "import json;f=open('$HOME/.dropbox/info.json', 'r').read();data=json.loads(f);print data.get('personal', {}).get('path', '')")

    BASE_PATH="$DROPBOX_PERSONAL/blog/content"
    IMAGE_PATH="images"
    SEARCH_PATH="$BASE_PATH/$IMAGE_PATH"

    LAST_ADDED=$(mdfind \
        -onlyin "$SEARCH_PATH" \
        'kMDItemDateAdded >= $time.today(-1)' \
        -attr 'kMDItemDateAdded' | \
    awk -F"kMDItemDateAdded =" '{print $2 "|" $1}' |
    sort -r | \
    cut -d'|' -f2 | \
    head -n1 | \
    sed -e 's/^ *//' -e 's/ *$//' -e "s:$BASE_PATH::")

    echo -n "![]({static}$LAST_ADDED)"
