from os import walk
from os.path import isfile, join, splitext, realpath, expanduser
from os.path import split as splitdir
import codecs

outdir = join(expanduser("~"),"Desktop")
TVShows = "V:\\TV Shows"
Movies = "V:\\Movies"

def indexfiles(rootdir,outputfilepath):
    totalfiles = 0
    outputfilename = "_" + rootdir.replace(':','').replace('\\','.') + ".txt"
    with codecs.open(join(outputfilepath,outputfilename), "w", encoding='utf8') as output:
        filetypes = []
        #files = []
        for (dirname, subdirlist, filelist) in walk(rootdir):
            subdirlist.sort()
            filelist.sort()
            for filename in filelist:
                ext = splitext(filename)[1]
                if ext not in [".ini", ".db", ".txt", ".py", ".pdf", ".png", ".jpg"]:
                
                    if ext not in filetypes:
                        filetypes.append(ext)
                    
                    totalfiles += 1
                    if dirname == rootdir:
                        output.write(filename + "\n")
                    else:
                        output.write(join(splitdir(dirname)[1], filename) + "\n")
                    #files.append(join(dirname[12:], filename))
        
    print("Number of files found: %s" % totalfiles)
    print("Observed filetypes: %s" % filetypes)
    print("Directory listings written to: \"" + outputfilename + "\" in directory " + outputfilepath)
    return join(outputfilepath, outputfilename)
    
        #output.write(str(filetypes))

def compbackup(origional, backup, rootdirs, outdir):
    difffile = "_diff.txt"
    with codecs.open(origional, 'r', encoding='utf8') as orig:
        with codecs.open(backup, 'r', encoding='utf8') as bak:
            bakfiles = set(bak)
            origfiles = set(orig)
            addedfiles = list(origfiles.difference(bakfiles))
            removedfiles = list(bakfiles.difference(origfiles))
            
    addedfiles.sort()
    removedfiles.sort()

    with codecs.open(join(outdir, difffile), 'w', encoding='utf8') as file_out:
        file_out.write("[ORG_DIR]**" + rootdirs[0] + "\n")
        file_out.write("[BAK_DIR]**" + rootdirs[1] + "\n\n\n")
        
        file_out.write("==== Added files ====\n")
        for line in addedfiles:
            file_out.write("[ADD]**" + line)
        file_out.write("\n\n====Removed files====\n")
        for line in removedfiles:
            file_out.write("[DEL]**" + line)
            
    print("\n\nA total of %s differences were found: %s new files and %s removed files." % (len(addedfiles)+len(removedfiles),len(addedfiles),len(removedfiles)))
    print("Differences written to: \"" + difffile + "\" in " + outdir)

            

[currentdir, currentfile] = splitdir(realpath(__file__))

if currentfile == "_movie_merge.py":
    rootdirs = [Movies,currentdir]
    
elif currentfile == "_show_merge.py":
    rootdirs = [TVShows,currentdir]
    
else:
    print(currentfile + " in " + currentdir)
    
    

print("\nScanning originals directory")
origional = indexfiles(rootdirs[0],outdir)
print("\n\nScanning backup directory")
backup = indexfiles(rootdirs[1],outdir)
    
compbackup(origional, backup, rootdirs, outdir)