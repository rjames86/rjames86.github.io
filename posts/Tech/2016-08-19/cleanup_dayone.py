#!/usr/bin/python

import codecs
import re
import sys
from datetime import datetime

input_file = sys.argv[1]

f = codecs.open(input_file,
                mode='r',
                encoding='utf-8').read()

# Get rid of the tabs that DayOne inserts
f = f.replace(u'\tDate:', 'Date:')
f = f.replace(u'\tWeather:', 'Weather:')
f = f.replace(u'\tLocation:', 'Location:')


# Replace default Markdown image syntax with Pelican's syntax + photos plugin
f = f.replace('![](photos/', '![]({photo}/')


title_re = re.compile(r'\n\n#\s+(.*)\n')
title_search = title_re.search(f)
now_datestring = datetime.now().strftime('%B %d, %Y at %H:%M:%S %Z')

# We need a title: header for Pelican
if title_search:
    f = 'Title: %s\n' % title_search.group(1) + f
    f = title_re.sub('', f) + "\n"
else:
    f = 'Title: Update %s\n' % now_datestring + f

if "Date:" not in f:
    f = "Date: %s\n" % now_datestring + f

with codecs.open(input_file, mode='w', encoding='utf-8') as new_file:
    new_file.write(f)
