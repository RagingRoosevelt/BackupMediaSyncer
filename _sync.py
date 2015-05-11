from os import remove, mkdir, listdir, rmdir
from os.path import join, expanduser, isdir
from os.path import split as splitdir
import codecs
from shutil import copy2

indir = join(expanduser("~"),"Desktop")
orgdir = ""
bakdir = ""

with codecs.open(join(indir,"_diff.txt"), 'r', encoding='utf8') as diff:

    # Read first line.  Should contain original directory
    line = diff.readline()
    try:
        line = line.replace("\n","").split("**")
        if line[0] == "[ORG_DIR]":
            orgdir = line[1]
    except:
        print("error: Bad logfile")
        quit()
        
    # Read second line.  Should contain backup directory
    line = diff.readline()
    try:
        line = line.replace("\n","").split("**")
        if line[0] == "[BAK_DIR]":
            bakdir = line[1]
    except:
        print("error: Bad logfile")
        quit()
        
    # If either of the directories weren't read in, then quit
    print("orig: %s, bak: %s" % (orgdir, bakdir))
    if orgdir == "" or bakdir == "":
        print("error: Bad logfile")
        quit()
    
    with codecs.open(join(indir,"_log.txt"), 'w', encoding='utf8') as log:
        log.write("Original directory: " + orgdir + "\n")
        log.write("Backup directory  : " + bakdir + "\n\n")
        
        for line in diff:
            if line.startswith("[ADD]"):
                line = line.replace("\n","").split("**")
                src = join(orgdir,line[1])
                dst = join(bakdir,line[1])
                if not isdir(splitdir(dst)[0]):
                    print("Directory \'" + splitdir(dst)[0] + "\' does not exist.  Creating directory.")
                    log.write("Directory \'" + splitdir(dst)[0] + "\' does not exist.  Creating directory.\n")
                    mkdir(splitdir(dst)[0])
                try:
                    print("Copying " + src + " to " + dst + "")
                    log.write("Copying " + src + " to " + dst + "\n")
                    copy2(src, dst)
                except:
                    print("error: %s not copied" % join(orgdir,line[1]))
                    log.write("error: " + join(orgdir,line[1]) + " not copied\n")
                    
            elif line.startswith("[DEL]"):
                line = line.replace("\n","").split("**")
                dst = join(bakdir,line[1])
                try:
                    print("Deleting " + dst + "")
                    log.write("Deleting " + dst + "\n")
                    remove(dst)
                    
                    if listdir(splitdir(dst)[0]) == []:
                        print("Directory " + splitdir(dst)[0] + "is empty, removing")
                        log.write("Directory " + splitdir(dst)[0] + "is empty, removing\n")
                        rmdir(splitdir(dst)[0])
                except:
                    print("error: %s not removed" % join(orgdir,line[1]))
                    log.write("error: " + join(orgdir,line[1]) + " not removed\n")
                    
            elif line.startswith("====Removed files===="):
                print("\n\n")
                log.write("\n\n")
                
        
