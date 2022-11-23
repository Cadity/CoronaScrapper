import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from Scrapper.WriteData import MainFunction, Etape_E, WriteFile

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.table = TableCnv(self, width = 1000, height = 250)
        self.table.pack()

        proteinList =["Protéine Spike", "Protéine N", "Protéine M"]

        def changeTableCurrent(event):
            selectedGen = listeCombo.get().split("Protéine ")[1]
            msgBox = messagebox.showinfo(title="Table à jour", message="Le tableau à correctement été mis à jour avec le gène " + selectedGen)

            if selectedGen == "Spike":
                self.table.currentGene = "S"
            else:
                self.table.currentGene = selectedGen

            WriteFile(self.table.currentGene)
            self.table.defaultTab()

        btn = tk.Button(self, text="Table des virus", command=self.table.defaultTab)
        btn.pack()

        btn = tk.Button(self, text="Table des gènes", command=self.table.genTable)
        btn.pack()

        btn = tk.Button(self, text="Comparaison des nucléotides", command=self.table.nucCompare)
        btn.pack()

        listeCombo = Combobox(self, values=proteinList)
        listeCombo.current(0)
        listeCombo.pack()
        listeCombo.bind('<<ComboboxSelected>>', changeTableCurrent)

class TableCnv(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.currentGene = "S"
        self.resultList = MainFunction(self.currentGene, True)
        self.dataList = self.resultList[0]
        self.errorList = self.resultList[1]

        self.labelText = tk.StringVar()
        self.labelText.set("")
        self.protTitle = tk.Label(self, textvariable=self.labelText).place(relx=0.05, rely=0.05, anchor="nw")

        self.tableau = Treeview(self, columns=('','virus1', 'virus2', 'virus3'))
        self.tableau.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.9)
        self.defaultTab()
        
    def defaultTab(self):
        self.clear()

        self.labelText.set("Analyse des virus : ")

        #self.protTitle = tk.Label(self, text="Analyse de la protéine ").place(relx=0.05, rely=0.05, anchor="nw")
        self.tableau.heading('virus1', text=self.dataList[1][0])
        self.tableau.heading('virus2', text=self.dataList[1][1])
        self.tableau.heading('virus3', text=self.dataList[1][2])
        self.tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
       
        self.tableau.insert('', 'end', values=("Organisme", self.dataList[2][0], self.dataList[2][1], self.dataList[2][2]))
        self.tableau.insert('', 'end', values=("Identifiant", self.dataList[3][0], self.dataList[3][1], self.dataList[3][2]))
        self.tableau.insert('', 'end', values=("Numéro GenBank", self.dataList[4][0], self.dataList[4][1], self.dataList[4][2]))
        self.tableau.insert('', 'end', values=("Date de Création GenBank", self.dataList[5][0], self.dataList[5][1], self.dataList[5][2]))
        self.tableau.insert('', 'end', values=("Nombre de gènes", self.dataList[6][0], self.dataList[6][1], self.dataList[6][2]))
        self.tableau.insert('', 'end', values=("Taux de GC (%)", self.dataList[7][0], self.dataList[7][1], self.dataList[7][2]))

    def genTable(self):
        self.clear()

        self.labelText.set("Gènes localisés dans les Coronavirus : ")

        self.tableau.heading('virus1', text="Identifiant")
        self.tableau.heading('virus2', text="Position de départ")
        self.tableau.heading('virus3', text="Position de fin")
        self.tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert

        count = 0
        for a in range(self.dataList[0]):
            self.tableau.insert('', 'end', values=(self.dataList[1][a], "", "", ""))
            for x in range(count, count + self.dataList[6][a]):
                self.tableau.insert('', 'end', values=(self.dataList[8][x], self.dataList[9][x], self.dataList[10][x], self.dataList[11][x]))
            count = count + self.dataList[6][a] # Addition de count et du nombre de gène -> Nouveau point de départ

    def clear(self):
        for item in self.tableau.get_children():
            self.tableau.delete(item)

    def nucCompare(self):
        self.clear()

        self.resultList = Etape_E(self.currentGene)

        self.labelText.set("Taux de conservation de la protéine " + self.currentGene + " : " + str(self.resultList[4]) + " %, pour la chauve souris, " + str(self.resultList[5]) + " %, pour le Pangolin")

        self.tableau.heading('virus1', text="Homme")
        self.tableau.heading('virus2', text="Chauve-Souris")
        self.tableau.heading('virus3', text="Pangolin")

        for a in range(len(self.resultList[0])):
            self.tableau.insert('', 'end', values=(self.resultList[0][a], self.resultList[1][a], self.resultList[2][a], self.resultList[3][a]))
        
def Display():
    # Window Settings
    root = tk.Tk()
    root.geometry("1000x500")
    root.title("Résultat d'analyse du fichier GenBank")
    root.resizable(False, False)

    # DataList init
    #result = MainFunction("S", True)
    #dataList = result[0]

    # Label
    firstTitle = tk.Label(root, text="Résultat d'analyse du fichier GenBank : ").place(relx=0.02, rely=0.02, anchor="nw")
    #seqNumber = tk.Label(root, text="Nombre de séquences : " + str(dataList[0])).place(relx=0.05, rely=0.12, anchor="nw")
    genBankPath = tk.Label(root, text="Fichier de référence GenBank : seq_covid.txt").place(relx=0.05, rely=0.16, anchor="nw")
    pathDoc = tk.Label(root, text="Emplacement du document de référence : info_seq-covid.txt").place(relx=0.05, rely=0.20, anchor="nw")
    titleTable1 = tk.Label(root, text="Tableau récapitulatif des informations sur les Coronavirus").place(relx=0.05, rely=0.27, anchor="nw")

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

    # Gif
    from PIL import Image, ImageTk
    image1 = Image.open("Resources/Cov.png")
    image1 = image1.resize((100, 100))
    test = ImageTk.PhotoImage(image1)

    label1 = tk.Label(image=test)
    label1.image = test
    label1.place(relx=0.8, rely=0.04)

    win = App(root)
    win.place(anchor="center", relx=0.5, rely=0.63)
    root.mainloop()
