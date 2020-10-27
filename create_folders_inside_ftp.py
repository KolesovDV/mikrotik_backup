import sys
import os
import shutil

# Create directory 
def ftpmkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        print ("imposible to create %s folder" % path)
    else:
        print ("Folder %s created successfully" % path)

def ftpmvdir(path1, path2):
    try:
        shutil.move(path1,path2)
    except OSError:
        print ("imposible to move from " % path1)
    else:
        print ("Files successfully moved")
