import os
from os import path
from datetime import datetime

global rules
rules = False

filePath = "Fichiers externes"
    
def MakeLogs(text):
    if rules == True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:%f")[:-3]
        
        result = current_time + " -> " + text

        file = open(filePath + "/Logs/" + "Logs.txt", "r")
        currentString = file.read()
        file.close()
        file = open(filePath + "/Logs/" + "Logs.txt", "w")
        file.write(result + "\n" + currentString)
        file.close()

def NewSession():
    if rules == True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:%f")[:-3]
        file = open(filePath + "/Logs/" + "Logs.txt", "r")
        currentString = file.read()
        file.close()
        file = open(filePath + "/Logs/" + "Logs.txt", "w")
        newSessionString = "Détail de la session :\n{\n\tOuverture : " + current_time + "\n}" + "\n-------------- Nouvelle Session -------------- \n"

        file.write(newSessionString + "\n" + currentString)
        file.close()

def AllowLogs(value):
    global rules
    rules = value

def ClearLogs():
    file = open(filePath + "/Logs/" + "Logs.txt", "w")
    file.write("")
    file.close()