import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from Scrapper.WriteData import MainFunction

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.table = TableCnv(self, width = 1000, height = 230)
        self.table.pack()

        proteinList =["Protéine Spike", "Protéine N", "Protéine M"]
        listeCombo = Combobox(self, values=proteinList)
        listeCombo.current(0)
        listeCombo.pack()

        def changeTableCurrent(event):
            selectedGen = listeCombo.get().split("Protéine ")[1]
            msgBox = messagebox.showinfo(title="Table à jour", message="Le tableau à correctement été mis à jour avec le gène " + selectedGen)

            if selectedGen == "Spike":
                self.table.currentGene = "S"
            else:
                self.table.currentGene = selectedGen

        listeCombo.bind('<<ComboboxSelected>>', changeTableCurrent)

        btn = tk.Button(self, text="Table des virus", command=self.table.defaultTab)
        btn.pack()

        btn = tk.Button(self, text="Table des gènes", command=self.table.genTable)
        btn.pack()

        btn = tk.Button(self, text="Comparaison des nucléotides", command=self.table.nucCompare)
        btn.pack()

class TableCnv(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.currentGene = "S"
        self.resultList = MainFunction(self.currentGene)
        self.dataList = self.resultList[0]
        self.errorList = self.resultList[1]

        self.tableau = Treeview(self, columns=('','virus1', 'virus2', 'virus3'))
        self.defaultTab()
        
    def defaultTab(self):
        self.clear()
        self.tableau.heading('virus1', text=self.dataList[1][0])
        self.tableau.heading('virus2', text=self.dataList[1][1])
        self.tableau.heading('virus3', text=self.dataList[1][2])
        self.tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
        self.tableau.place(relx=0.5, rely=0.49, anchor="center", relwidth=0.9)
        self.tableau.insert('', 'end', values=("Organisme", self.dataList[2][0], self.dataList[2][1], self.dataList[2][2]))
        self.tableau.insert('', 'end', values=("Identifiant", self.dataList[3][0], self.dataList[3][1], self.dataList[3][2]))
        self.tableau.insert('', 'end', values=("Numéro GenBank", self.dataList[4][0], self.dataList[4][1], self.dataList[4][2]))
        self.tableau.insert('', 'end', values=("Date de Création GenBank", self.dataList[5][0], self.dataList[5][1], self.dataList[5][2]))
        self.tableau.insert('', 'end', values=("Nombre de gènes", self.dataList[6][0], self.dataList[6][1], self.dataList[6][2]))
        self.tableau.insert('', 'end', values=("Taux de GC (%)", self.dataList[7][0], self.dataList[7][1], self.dataList[7][2]))

    def genTable(self):
        self.clear()
        self.tableau.heading('virus1', text="Identifiant")
        self.tableau.heading('virus2', text="Position de départ")
        self.tableau.heading('virus3', text="Position de fin")
        self.tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
        self.tableau.place(relx=0.5, rely=0.49, anchor="center", relwidth=0.9)

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

        self.resultList = MainFunction(self.currentGene)
        self.errorList = self.resultList[1]

        self.tableau.heading('virus1', text="Homme")
        self.tableau.heading('virus2', text="Chauve-Souris")
        self.tableau.heading('virus3', text="Pangolin")

        for a in range(len(self.errorList[0])):
            self.tableau.insert('', 'end', values=(self.errorList[0][a], self.errorList[1][a], self.errorList[2][a], self.errorList[3][a]))

def Display():
    # Window Settings
    root = tk.Tk()
    root.geometry("1000x500")
    root.title("Résultat d'analyse du fichier GenBank")
    root.resizable(False, False)

    # DataList init
    result = MainFunction("S")
    dataList = result[0]
    # Label
    firstTitle = tk.Label(root, text="Résultat d'analyse du fichier GenBank : ").place(relx=0.02, rely=0.02, anchor="nw")
    seqNumber = tk.Label(root, text="Nombre de séquences : " + str(dataList[0])).place(relx=0.05, rely=0.12, anchor="nw")
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
    label1.place(relx=0.8, rely=0.05)


    win = App(root)
    win.place(anchor="center", relx=0.5, rely=0.6)
    root.mainloop()
