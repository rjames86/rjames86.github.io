#!/bin/bash

url=$(echo %clipboard | sed 's/www.dropbox.com/dl.dropboxusercontent.com/g' | tr -d '\n')

echo "$url"
