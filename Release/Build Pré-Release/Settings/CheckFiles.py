import os
from os import path
from datetime import datetime
from Settings.WriteSettings import WriteNewSettings

filePath = "Fichiers externes"

def LoadFile():
    CheckPath()

def CheckPath():
    if path.exists(filePath) == False:
        os.mkdir(filePath)

    if path.exists(filePath + "/Logs") == False:
        os.mkdir(filePath + "/Logs")
    
    if path.exists(filePath + "/Logs/" + "Logs.txt") == False:
        CreateLogsFile()

    if path.exists(filePath + "/Paramètres") == False:
        os.mkdir(filePath + "/Paramètres")

    if path.exists("Fichiers externes/Paramètres" + "/Paramètres.txt") == False:
        WriteNewSettings((1, 1, 1, 0))

def CreateLogsFile():
    file = open(filePath + "/Logs/" + "Logs.txt", "w")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")[:-3]
    file.write(current_time + " -> Le fichier de Log à été créé")
    file.close()
