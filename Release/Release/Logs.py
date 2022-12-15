import os
from os import path
from datetime import datetime

global rules # Règles globales
rules = False

filePath = "Fichiers externes" # Chemin du répertoire principal
    
def MakeLogs(text):
    if rules == True: # Si on peut écrire dans les logs
        now = datetime.now() # Récupération de la date actuelle
        current_time = now.strftime("%H:%M:%S:%f")[:-3] # Sous cette forme
        
        result = current_time + " -> " + text

        file = open(filePath + "/Logs/" + "Logs.txt", "r")
        currentString = file.read()
        file.close()
        file = open(filePath + "/Logs/" + "Logs.txt", "w")
        file.write(result + "\n" + currentString)
        file.close()

def NewSession(): # A la nouvelle session, on écrit un message dans les logs
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

def AllowLogs(value): # Changement de la règle globale d'écriture dans les logs
    global rules
    rules = value

def ClearLogs(): # Fonction qui permet de clear ("nettoyer") les logs
    file = open(filePath + "/Logs/" + "Logs.txt", "w")
    file.write("")
    file.close()

def Event(text):
    file = open(filePath + "/Logs/" + "Logs.txt", "r")
    currentString = file.read()
    file = open(filePath + "/Logs/" + "Logs.txt", "w")
    file.write("\n---- " + text + " ----\n" + currentString)
    file.close()