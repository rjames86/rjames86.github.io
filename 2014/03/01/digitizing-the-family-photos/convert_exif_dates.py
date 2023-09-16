"""
This script is to take folders of images and add exif timestamps to them. The folder structure should look like:

January 1990
    - image1.jpg
    - image2.jpg

Alternatively, the folder name can look like "January-February 1990" but the script will use the first month name
for the date.

"""

import os
import re
import datetime
import subprocess
from os.path import join

HOME = os.path.expanduser('~')

# /Users/rjames/Dropbox (Personal)/Pictures/Scans of Negatives/Low Res JPGs
JPG_FOLDER = join(HOME,\
    'Dropbox', 'Scans of Negatives', 'Low Res JPGs')

ALBUM_FOLDERS = [f for f in os.listdir(JPG_FOLDER)
                    if os.path.isdir(join(JPG_FOLDER, f))]
skipped_folders = []

def skip_folder(folder):
    print "Skipping folder: ", folder
    skipped_folders.append(folder)

print "====== PROCESSING FOLDERS ======"
print "\n".join(ALBUM_FOLDERS)
print "=" * 32

for folder in ALBUM_FOLDERS:
    """Find folders that look like this January 1990 or January-February 1990"""
    search = re.search(r'([A-Za-z]+[-[A-Za-z]+]?) ([0-9]+)', folder)

    if not search:
        skip_folder(folder)
        continue
    else:
        month = search.group(1)
        year = search.group(2)

        try:
            month_to_int = datetime.datetime.strptime(month.split('-')[0], '%B')
        except:
            skip_folder(folder)
            continue

        exif_datestring = "%s:%02d:01 12:00:00" % (year, month_to_int.month)
        touch_datestring = "%s%02d011200" % (year, month_to_int.month)
        confirm_date = raw_input("%s: %s" % (folder, exif_datestring))
        
        if not confirm_date:
            # exiftool "-AllDates=1986:11:05 12:00:00" foldername/
            df = subprocess.Popen([
                    'exiftool',\
                    '-AllDates=%s' % exif_datestring,\
                    join(JPG_FOLDER, folder)], 
                stdout=subprocess.PIPE)
            print "Setting Exif dates..."
            df.communicate()
        
            print "Setting creation dates..."
            df = subprocess.Popen([
                    'touch',\
                    '-t',\
                    touch_datestring,\
                    join(JPG_FOLDER, folder + '/*',)], 
                stdout=subprocess.PIPE)
            df.communicate()


print "Skipped folders: ", ", ".join(skipped_folders)
print "Folders processed: ", len(ALBUM_FOLDERS) - len(skipped_folders)

print "=====STARTING SKIPPED FOLDERS ====="
print "\n".join(skipped_folders)
print "\n"

for folder in skipped_folders:
    confirm_date = raw_input("%s: %s" % (folder, exif_datestring)) + " 12:00:00"
    while not re.search(r'\d{4}(:\d{2}){2} 12:00:00', confirm_date):
        confirm_date = raw_input("%s: %s" % (folder, exif_datestring)) + " 12:00:00"

    df = subprocess.Popen([
            'exiftool',\
            '-AllDates=%s' % confirm_date,\
            join(JPG_FOLDER, folder)], 
        stdout=subprocess.PIPE)
    df.communicate()


def sanity_check():
    for folder in ALBUM_FOLDERS:
        jpgs = [j for j in os.listdir(join(JPG_FOLDER, folder)) if 'jpg' in j]
        originals = len([o for o in jpgs if '_original' in o])
        edited = len([e for e in jpgs if not '_original' in e])
        if originals and (originals != edited):
            print folder
            print "Original count: ", originals
            print "Edited count: ", edited
            print '-' * 15, '\n'
        else:
            print "All Good: ", folder
