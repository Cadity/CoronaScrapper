import tkinter as tk
from tkinter import messagebox
from Settings.WriteSettings import WriteNewSettings
from Logs import MakeLogs

isClosed = True # On défini isClosed ; Cette variable permet de savoir si la fenêtre est fermée par l'utilisateur ou par un bouton

def DisplaySettings(setList):
    global oldSettingsList
    oldSettingsList = list()
    global mafftCommandLine, usingLogs, rewritingFile, keepOldLogs, CreateAllFiles
    oldSettingsList = setList
    mafftCommandLine = oldSettingsList[0]
    usingLogs = oldSettingsList[1]
    rewritingFile = oldSettingsList[2]
    keepOldLogs = oldSettingsList[3]
    CreateAllFiles = oldSettingsList[4]
    #Définition de la fenêtre
    Settings = tk.Tk()
    Settings.geometry("500x250")
    Settings.title("Paramètres")
    Settings.resizable(False, False); #Règle Resizable définie sur False => Limite les erreurs d'affichages car labels statiques
    Settings.eval('tk::PlaceWindow . center')
    
    #Définition des Label
    title = tk.Label(Settings, text="Appuyez sur sauvegarder pour appliquer les changements").place(relx = 0.02,rely = 0.75,anchor ='nw')
    saveButton = tk.Button(Settings, text="Sauvegarder", relief="raised", command=lambda:[QuitWindow(), Settings.destroy()]).place(relx = 0.97,rely = 0.95, anchor ='se')
    #Définition des boutons à cocher

    check_1 = tk.IntVar()
    check_2 = tk.IntVar()
    check_3 = tk.IntVar()
    check_4 = tk.IntVar()
    check_5 = tk.IntVar()

    check_1.set(oldSettingsList[0])
    check_2.set(oldSettingsList[1])
    check_3.set(oldSettingsList[2])
    check_4.set(oldSettingsList[3])
    check_5.set(oldSettingsList[4])

    def modifyMafftCmdLine():
        global mafftCommandLine
        if check_1.get() == 1:
            mafftCommandLine = 1
        else :
            mafftCommandLine = 0

    def modifyUsingLogs():
        global usingLogs
        if check_2.get() == 1:
            usingLogs = 1
        else :
            usingLogs = 0

    def modifyRewritingFiles():
        global rewritingFile
        if check_3.get() == 1:
            rewritingFile = 1
        else :
            rewritingFile = 0

    def modifyKeepOldLogs():
        global keepOldLogs
        if check_4.get() == 1:
            keepOldLogs = 1
        else :
            keepOldLogs = 0

    def modifyCreateAllFiles():
        global CreateAllFiles
        if check_5.get() == 1:
            CreateAllFiles = 1
        else :
            CreateAllFiles = 0

    check_button_1 = tk.Checkbutton(Settings, text = "Utiliser MafftCommandLine (Décocher pour l'Etape K)", variable = check_1, onvalue = 1, offvalue = 0, command=modifyMafftCmdLine).place(relx = 0.02,rely = 0.07,anchor ='nw')
    check_button_2 = tk.Checkbutton(Settings, text = "Utiliser des fichiers de Logs", variable = check_2, onvalue = 1, offvalue = 0, command=modifyUsingLogs).place(relx = 0.02,rely = 0.20,anchor ='nw')
    check_button_3 = tk.Checkbutton(Settings, text = "Réécrire les fichiers", variable = check_3, onvalue = 1, offvalue = 0, command=modifyRewritingFiles).place(relx = 0.02,rely = 0.33,anchor ='nw')
    check_button_4 = tk.Checkbutton(Settings, text = "Conserver les anciens Logs", variable = check_4, onvalue = 1, offvalue = 0, command=modifyKeepOldLogs).place(relx = 0.02,rely = 0.46,anchor ='nw')
    check_button_5 = tk.Checkbutton(Settings, text = "Télécharger et créer l'ensemble des fichiers", variable = check_5, onvalue = 1, offvalue = 0, command=modifyCreateAllFiles).place(relx = 0.02,rely = 0.59,anchor ='nw')

    Settings.mainloop()
    global isClosed
    return isClosed
    
def QuitWindow():
    global isClosed
    isClosed = False
    newSetList = list()
    newSetList.append(mafftCommandLine)
    newSetList.append(usingLogs)
    newSetList.append(rewritingFile)
    newSetList.append(keepOldLogs)
    newSetList.append(CreateAllFiles)

    willBeRewriting = False
    if oldSettingsList[0] != mafftCommandLine:
        willBeRewriting = True
    if oldSettingsList[1] != usingLogs:
        willBeRewriting = True
    if oldSettingsList[2] != rewritingFile:
        willBeRewriting = True
    if oldSettingsList[3] != keepOldLogs:
        willBeRewriting = True
    if oldSettingsList[4] != CreateAllFiles:
        willBeRewriting = True

    if willBeRewriting == True:
        WriteNewSettings(newSetList)
    else:
        MakeLogs("Les paramètres n'ont pas été changés ; Le fichier n'a pas été réécrit")
