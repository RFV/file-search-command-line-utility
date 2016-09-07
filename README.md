# file-search-command-line-utility
Command line utility in Python for OS X that does specific file searches based on contents of files, including, datetime, size, contents, etc
Need to have developed a command line utility in Python for OS X. 

The utility will take as input (source) as list of files and/or folders, or a file containing same, and search another (target) list of file and/or folders, or a file containing same, to see if the source file(s) are found anywhere in the target location(s). 

The determination of a match includes name, create timestamp, modification timestamp, file size, file hash, and file attributes. Source and/or target files may begin with a period "." meaning that they are normally invisible in the Finder.

The output is a list with tab separated fields as follows: source file location, target file location. A source file may be found in more than one target file location. If the source file is not found in any target file location, then the default text of "not found" should be used in place of the target file location.

An optional argument to the utility will move source file(s) to the Finder Trash (not delete). Source file(s) and target location(s) may be on remotely mounted drives, so the optional "move to trash" feature will need to determine if this is the case, and, if so, "move to trash" on the remote volume and not "move to trash" on the target volume which would force a cross-volume move.

Sample arguments:

utilityname -i filename1 filename2 -o location1 location2 
utilityname -if filelist_i -o location1 location2
utilityname -i filename1 -of filelist_o
utilityname -if filelist_i -of filelist_o
utilityname -if filelist_i -of filelist_o -trash

-i	  indicates that one or more source filenames and/or directories follow
-if	  indicates that the filename that follows contains a list of one or more source filenames and/or directories, and should be used as if they were provided via -i
-o	  indicates that one or more target filenames and/or directories follow
-of	  indicates that the filename that follows contains a list of one or more target filenames and/or directories, and should be used as if they were provided via -o
-trash	  indicates that matching source filename and/or directories should be moved to Finder Trash
-noempty  indicates that directories left empty as a result of -trash (ignoring the .DS_Store file) should also be  moved to the Finder Trash

Execution statistics should also be provided: Time from start to finish, total number of source files checked, total number of target locations checked, total number of matches, total number of non-matches, percentage of matches to total number of source files checked.

Platform is running OS X 10.11.5 El Capitan.

Work effort will be considered complete upon receiving a working and tested version, along with the Python source.
