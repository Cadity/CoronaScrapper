from Window.Intro import DisplayIntro
from Window.MainWindow import Display
from Scrapper.ScrapData import PingCheck, GetData
from Scrapper.WriteData import MainFunction
from tkinter import filedialog, messagebox

def main():
    result = DisplayIntro() #On affiche la fenêtre d'introduction

    if result == False: #Si la règle isClosed est fausse (donc que le fenêtre n'est pas fermé soit avec le clavier soit avec la "Croix")
        if PingCheck() == 0: # On effectue un test de ping ; Si retourné faux, on affiche à nouveau la fenêtre principale
            main()
            # Sinon, on passe à GetData qui récupère le fichier à l'aide du scrapper
    else:
        quit()

    if GetData() == False: # Contrôle en cas de dysfonctionnement du test de ping mais normalement GetData renverra toujours vrai
        msgBox = messagebox.showerror(title="Erreur d'Acquisition", message="Aucune réponse n'a émanée du serveur")
        main()
        
    dataList = MainFunction() # On récupère la liste des informations obtenus depuis seq_covid et on écris dans info_seq_covid
    Display() # On affiche la fenêtre principale et on donne en argument la liste obtenue

main()