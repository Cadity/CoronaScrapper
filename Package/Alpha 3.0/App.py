from Window.Intro import DisplayIntro
from Window.MainWindow import Display
from Scrapper.ScrapData import PingCheck, GetData
from Scrapper.WriteData import MainFunction
from tkinter import filedialog, messagebox

def main():
    result = DisplayIntro() #On affiche la fenêtre d'introduction

    if result == False: #Si la règle isClosed est fausse (donc que le fenêtre n'est pas fermé soit avec le clavier soit avec la "Croix")
        if PingCheck() == 0:
            main()
    else:
        quit()

    if GetData() == False:
        msgBox = messagebox.showerror(title="Erreur d'Acquisition", message="Aucune réponse n'a émanée du serveur")
        main()
        
    dataList = MainFunction()
    Display(dataList)

main()