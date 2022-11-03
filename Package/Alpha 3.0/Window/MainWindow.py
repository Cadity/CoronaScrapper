import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog

def Display(dataList):
    #Définition de la fenêtre
    root = tk.Tk()
    root.geometry("900x500")
    root.title("Résultat d'analyse du fichier GenBank")
    root.resizable(False, False)

    #Menu
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    menufichier = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Fichier", menu=menufichier)
    menufichier.add_command(label = "Importer unr fichier")
    menufichier.add_command(label = "Exporter au format txt")
    menufichier.add_separator()
    menufichier.add_command(label = "Quitter", command=root.destroy)

    menuprofile = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label = "Utilisateur", menu=menuprofile)
    menuprofile.add_command(label="Preset 1")
    menuprofile.add_command(label="Preset 2")
    menuprofile.add_command(label="Preset 3")
    #Fin Menu

    #Title Label
    firstTitle = tk.Label(root, text="Résultat d'analyse du fichier GenBank : ").place(relx=0.02, rely=0.02, anchor="nw")
    seqNumber = tk.Label(root, text="Nombre de séquences : " + str(dataList[0])).place(relx=0.05, rely=0.12, anchor="nw")
    genBankPath = tk.Label(root, text="Fichier de référence GenBank : seq_covid.txt").place(relx=0.05, rely=0.16, anchor="nw")
    pathDoc = tk.Label(root, text="Emplacement du document de référence : info_seq-covid.txt").place(relx=0.05, rely=0.20, anchor="nw")
    titleTable1 = tk.Label(root, text="Tableau récapitulatif des informations sur les Coronavirus").place(relx=0.05, rely=0.27, anchor="nw")

    #Tableau Récapitulatif
    
    tableau = Treeview(root, columns=('','virus1', 'virus2', 'virus3'))
    tableau.heading('virus1', text=dataList[1][0])
    tableau.heading('virus2', text=dataList[1][1])
    tableau.heading('virus3', text=dataList[1][2])
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.place(relx=0.5, rely=0.53, anchor="center", relwidth=0.9)
    tableau.insert('', 'end', values=("Organisme", dataList[2][0], dataList[2][1], dataList[2][2]))
    tableau.insert('', 'end', values=("Identifiant", dataList[3][0], dataList[3][1], dataList[3][2]))
    tableau.insert('', 'end', values=("Numéro GenBank", dataList[4][0], dataList[4][1], dataList[4][2]))
    tableau.insert('', 'end', values=("Date de Création GenBank", dataList[5][0], dataList[5][1], dataList[5][2]))
    tableau.insert('', 'end', values=("Nombre de gènes", dataList[6][0], dataList[6][1], dataList[6][2]))
    tableau.insert('', 'end', values=("Taux de GC (%)", dataList[7][0], dataList[7][1], dataList[7][2]))
 

    #Display de la fenêtre
    root.mainloop()