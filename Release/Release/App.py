from Window.Intro import DisplayIntro, RedefineSelected
from Window.MainWindow import Display
from Scrapper.ScrapData import PingCheck, GetData
from Window.Settings import DisplaySettings
from tkinter import messagebox
from Logs import MakeLogs
from Settings.ReadSettings import ReadSet
from Settings.CheckFiles import LoadFile
from Scrapper.WriteData import Main

# Définition des variables
global firstLoading # Cette variable permet de savoir si le programme viens d'être lancé ou s'il y a eu un retour au menu
firstLoading = True

global setList # Cette variable permet de définir la liste de paramètres pour la changer à chaque fois
setList = list()

global dataList # Cette variable permet de conserver les données récupérés afin de les afficher
dataList = list()

def main():
    global firstLoading, setList, genList, dataList
    if firstLoading == True:
        setList = ReadSet(True)
        firstLoading = False
        MakeLogs("CoronaWrapper à été généré avec succès")  
    else:
        setList = ReadSet(False)

    result = DisplayIntro() #On affiche la fenêtre d'introduction

    if result == "activatingProcess": #Si la règle isClosed est fausse (donc que le fenêtre n'est pas fermé soit avec le clavier soit avec la "Croix")
        if PingCheck() == 0: # On effectue un test de ping ; Si retourné faux, on affiche à nouveau la fenêtre principale
            main()
            # Sinon, on passe à GetData qui récupère le fichier à l'aide du scrapper
    elif result == "settingsSelected":
        setResult = DisplaySettings(setList)
        RedefineSelected()
        if setResult == True:
            quit()
        else:
            main()
    else:
        quit()

    if GetData() == False: # Contrôle en cas de dysfonctionnement du test de ping mais normalement GetData renverra toujours vrai
        msgBox = messagebox.showerror(title="Erreur d'Acquisition", message="Aucune réponse n'a émanée du serveur")
        main()

    if(len(dataList) == 0):
        dataList = Main.EntryPoint()

    Display(dataList) # On affiche la fenêtre principale et on donne en argument la liste obtenue
    RedefineSelected()
    main()

LoadFile()
main()



