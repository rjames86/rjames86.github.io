#! /usr/bin/env python -i

import os, re, sys
#import Growl
import datetime

path_dropbox = os.path.join(os.path.expanduser("~"), "Dropbox", "Shared Folders", "Scans of Negatives")
path_desktop = os.path.join(os.path.expanduser("~"), "Desktop", "Scans of Negatives")

filenames = os.listdir(path_dropbox)

def d_from_dt(dt):
    return '%02i/%02i/%02i %02i:%02i'  % (dt.year, dt.month, dt.day,dt.hour, dt.minute)

now_unformat = datetime.datetime.now()

now = d_from_dt(now_unformat)

for file in filenames:
    if "." in file:
        invis = filenames.index(file)
        filenames.pop(invis)
        
filelist = []
def main(): 
    f = open('/Users/user/Dropbox/.log.txt', 'a')
    f.write('Run time: ' + now + '\n')
    
    
    for file in filenames:
        if not os.path.exists(os.path.join(path_desktop, file)):
            os.mkdir(os.path.join(path_desktop, file))
        for psds in os.listdir(os.path.join(path_dropbox, file)):
            if ".DS_Store" in psds:
                continue
            else:
                filelist.append(psds)
        
    if len(filelist) < 1:
        f.write('\tNo Files were moved\n')
    else:
        for file in filenames:
            for psds in os.listdir(os.path.join(path_dropbox, file)):
                if ".DS_Store" in psds:
                    continue
                else:
                    os.rename(os.path.join(path_dropbox, file, psds), os.path.join(path_desktop, file, psds))
                    title = psds + " was moved to:"
                    os.system("/usr/local/bin/growlnotify -t \"" + title + "\" -m \"" + os.path.join(path_desktop, file) + "\"")
                    f.write('\t' + psds + " was moved to " + file + '\n')
    
        
    f.close()

if __name__ == "__main__":
    main()
