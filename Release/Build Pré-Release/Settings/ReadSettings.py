from Logs import AllowLogs
from Logs import MakeLogs, NewSession, ClearLogs

def ReadSet(isFirstLoad):
    file = open("Fichiers externes/Paramètres" + "/Paramètres.txt", "r")
    result = file.read().split("\n")
    file.close()

    mafftCommandLine = 0
    mafftCmdLineString = "False"
    usingLogs = 0
    usingLogsString = "False"
    rewritingFile = 0
    rewritingFileString = "False"
    keepOldLogs = 1
    keepOldLogsString = "False"

    try:  
        if result[0].split("mafftCommandLine : ")[1] == "True":
            mafftCommandLine = 1
            mafftCmdLineString = "True"

        if result[1].split("usingLogs : ")[1] == "True":
            AllowLogs(True)
            usingLogs = 1
            usingLogsString = "True"

        if result[2].split("rewritingFile : ")[1] == "True":
            rewritingFile = 1
            rewritingFileString = "True"

        if result[3].split("keepOldLogs : ")[1] == "False":
            keepOldLogs = 0
            keepOldLogsString = "False"

        if isFirstLoad == True:
            if keepOldLogs == 0:
                ClearLogs
            NewSession()

        setList = list()
        setList.append(mafftCommandLine)
        setList.append(usingLogs)
        setList.append(rewritingFile)
        setList.append(keepOldLogs)

        if isFirstLoad == True:
            MakeLogs("Les paramètres ont été chargés avec succès\n{\n\tmafftCommandLine = " + mafftCmdLineString + "\n\tusingLogs = " + usingLogsString + "\n\trewritingFile = " + rewritingFileString  + "\n\tkeepOldLogs = " + keepOldLogsString + "\n}")
    except Exception as e:
        MakeLogs("Erreur fatale\n{\n\tDescription : " + str(e) + "\n\tRésolution : Les paramètres par défaut ont été chargés\n}")
        return 0
    return setList
    