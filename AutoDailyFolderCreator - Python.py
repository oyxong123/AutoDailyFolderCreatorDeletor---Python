# Creates today's daily record folders.
# Runs daily at 0.00am with Task Scheduler
import os
import datetime
from win10toast_persist import ToastNotifier

# Set path of daily record folder locations.
loggedInUser = os.getlogin()
pathProgrammingLife = f"C:/Users/{loggedInUser}/Desktop/Programming Life"
pathLanguageCottage = f"C:/Users/{loggedInUser}/Desktop/Language Cottage"
pathMusicSquare = f"C:/Users/{loggedInUser}/Desktop/Music Square"
pathLife = f"C:/Users/{loggedInUser}/Desktop/Life"
pathUtp=  f"C:/Users/{loggedInUser}/Desktop/utp degree/Utp Life"
pathList = [pathProgrammingLife, pathLanguageCottage, pathMusicSquare, pathLife, pathUtp]
createdPaths = []
scriptStatus = True

try:
    # Create path if folder does not exist.
    for pathCurrent in pathList:
        
        # Create today's path.
        folderAdded = False
        dateToday = datetime.date.today().strftime("%Y_%m_%d")
        pathToday = os.path.join(pathCurrent, dateToday)
        if not os.path.exists(pathToday):
            os.makedirs(pathToday)
            folderAdded = True
            
        # Special operations for language cottage.
        if pathCurrent == pathLanguageCottage:
            dir = os.listdir(pathToday)
            pathInner = os.path.join(pathToday, "oripic")
            if not os.path.exists(pathInner):
                os.makedirs(pathInner)
                folderAdded = True
          
        # Track created paths.
        if folderAdded:
            createdPaths.append(os.path.basename(pathCurrent))
        
except Exception as exception:
    scriptStatus = False
    errorMessage = str(exception)

# Convert created paths into full string. (only extract base part of path)
strCreatedPaths = ""
for createdPath in createdPaths:
    if strCreatedPaths != "":
        strCreatedPaths += ", "
    if len(createdPaths) > 1 and createdPath == createdPaths[-1]:
        strCreatedPaths += "and "
    if strCreatedPaths.count(",") == 1:
        strCreatedPaths.replace(",", "")
    
    # Gets the last name of the path.
    strCreatedPaths += os.path.basename(createdPath)

# Send notification of script state to windows.
notif = ToastNotifier()
if scriptStatus:
    if createdPaths:
        notif.show_toast("Auto Daily Folder Creator", "Operation Successful.\n" + dateToday + "\nCreated " + strCreatedPaths + ".", duration=5)
    else:
        notif.show_toast("Auto Daily Folder Creator", "Operation Successful.\n" + dateToday + "\nNo folders created.", duration=5)
    print("Script completed.") 
else:
    notif.show_toast("Auto Daily Folder Creator", "Operation Failed.\n" + dateToday + "\n" + errorMessage, duration=5)
    print("Script failed.") 
