from os import path
import os
from Logs import MakeLogs

def WriteNewSettings(setList):
    mafftCommandLine = setList[0]
    usingLogs = setList[1]
    rewritingFile = setList[2]
    keepOldLogs = setList[3]
    createAllFiles = setList[4]

    if mafftCommandLine == 1:
        mafftCommandLine = True
    else:
        mafftCommandLine = False

    if usingLogs == 1:
        usingLogs = True
    else:
        usingLogs = False

    if rewritingFile == 1:
        rewritingFile = True
    else:
        rewritingFile = False

    if keepOldLogs == 1:
        keepOldLogs = True
    else:
        keepOldLogs = False

    if createAllFiles == 1:
        createAllFiles = True
    else:
        createAllFiles = False

    setString = "mafftCommandLine : " + str(mafftCommandLine) + "\nusingLogs : " + str(usingLogs) + "\nrewritingFile : " + str(rewritingFile) + "\nkeepOldLogs : " + str(keepOldLogs) + "\ncreateAllFiles : " + str(createAllFiles)

    file = open("Fichiers externes/Paramètres" + "/Paramètres.txt", "w")
    file.write(setString)
    file.close()

    MakeLogs("Les paramètres ont été modifiés avec succès\n{\n\tmafftCommandLine = " + str(mafftCommandLine) + "\n\tusingLogs = " + str(usingLogs) + "\n\trewritingFile : " + str(rewritingFile) + "\n\tkeepOldLogs" + str(keepOldLogs) + "\n\tcreateAllFiles" + str(createAllFiles) + "\n}")


    