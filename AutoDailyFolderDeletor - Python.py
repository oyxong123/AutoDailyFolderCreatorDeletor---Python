# Deletes the record folders of today that contains no files.
# Runs daily at 0.00am with Task Scheduler
# Directory is equivalent to folder excluding files, also almost equivalent to path.
import os
import datetime
import shutil
import pandas as pd
from win10toast_persist import ToastNotifier

# Set path of daily record folder locations.
loggedInUser = os.getlogin()
pathProgrammingLife = f"C:/Users/{loggedInUser}/Desktop/Programming Life"
pathLanguageCottage = f"C:/Users/{loggedInUser}/Desktop/Language Cottage"
pathMusicSquare = f"C:/Users/{loggedInUser}/Desktop/Music Square"
pathLife = f"C:/Users/{loggedInUser}/Desktop/Life"
pathUtp=  f"C:/Users/{loggedInUser}/Desktop/utp degree/Utp Life"
pathArt = f"C:/Users/{loggedInUser}/Desktop/Artwork Room"
pathList = [pathProgrammingLife, pathLanguageCottage, pathMusicSquare, pathLife, pathUtp, pathArt]
deletedPaths = []
scriptStatus = True

try:
    # Delete path if directory contains no files.
    for pathCurrent in pathList:
        
        # Get yesterday's date path.
        fileExists = False
        innerFileExists = False
        dateToday = datetime.date.today()
        strDateYesterday = (dateToday - pd.Timedelta('1d')).strftime("%Y_%m_%d")
        pathYesterday = os.path.join(pathCurrent, strDateYesterday)
        
        # Skip check if yesterday's path is absent already.
        if not os.path.exists(pathYesterday):
            continue
        
        # Check whether each directory and their inner directories contain any files. (os.walk goes through all files and inner content of directories)
        for dirPath, dirNames, files in os.walk(pathYesterday): 
            if files:
                fileExists = True
                print(dirPath + " has files.")
            else:
                print(dirPath + " has no files.")
                        
        # Remove today's folder if no file is inside. (Set permission to force allow)
        if not fileExists:
            shutil.rmtree(pathYesterday, ignore_errors = True)
            deletedPaths.append(pathCurrent)

except Exception as exception:
    scriptStatus = False
    errorMessage = str(exception)

# Track which paths are deleted and turn it into a full string. (only extract base part of path)
strDeletedPaths = ""
for deletedPath in deletedPaths:
    if strDeletedPaths != "":
        strDeletedPaths += ", "
    if len(deletedPaths) > 1 and deletedPath == deletedPaths[-1]:
        strDeletedPaths += "and "
    if strDeletedPaths.count(",") == 1:
        strDeletedPaths.replace(",", "")
    
    # Gets the second last name of the path.
    strDeletedPaths += os.path.basename(deletedPath)

# Send notification of script state to windows.
notif = ToastNotifier()
if scriptStatus:
    if deletedPaths:
        notif.show_toast("Auto Daily Folder Deletor", "Operation Successful.\n" + strDateYesterday + "\nDeleted " + strDeletedPaths + ".", duration=5)
    else:
        notif.show_toast("Auto Daily Folder Deletor", "Operation Successful.\n" + strDateYesterday + "\nNo folders deleted.", duration=5)
    print("Script completed.") 
else:
    if deletedPaths:
        notif.show_toast("Auto Daily Folder Deletor", "Operation Failed.\n" + strDateYesterday + "\nDeleted " + strDeletedPaths + ".\n" + errorMessage, duration=5)
    else:
        notif.show_toast("Auto Daily Folder Deletor", "Operation Failed.\n" + strDateYesterday + "\n" + errorMessage, duration=5)
    print("Script failed.") 
