#!/bin/bash

cd ~/Dropbox/blogs/biketour/pelican_site

make publish

git add ..

git commit -am 'update blog'

/Users/rjames/dev/pelican/bin/ghp-import output

git push git@github.com:rjames86/rjames86.github.io.git gh-pages:master
