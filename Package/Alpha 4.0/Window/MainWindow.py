import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from Scrapper.WriteData import MainFunction

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.face = Face(self, width = 1000, height = 230)
        self.face.pack()

        btn = tk.Button(self, text="Table des virus", command=self.face.defaultTab)
        btn.pack()

        btn = tk.Button(self, text="Table des gènes", command=self.face.modify)
        btn.pack()

class Face(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)

        self.dataList = MainFunction()

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

    def modify(self):
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

def Display():
    # Window Settings
    root = tk.Tk()
    root.geometry("1000x500")
    root.title("Résultat d'analyse du fichier GenBank")
    root.resizable(False, False)

    # DataList init
    dataList = MainFunction()

    firstTitle = tk.Label(root, text="Résultat d'analyse du fichier GenBank : ").place(relx=0.02, rely=0.02, anchor="nw")
    seqNumber = tk.Label(root, text="Nombre de séquences : " + str(dataList[0])).place(relx=0.05, rely=0.12, anchor="nw")
    genBankPath = tk.Label(root, text="Fichier de référence GenBank : seq_covid.txt").place(relx=0.05, rely=0.16, anchor="nw")
    pathDoc = tk.Label(root, text="Emplacement du document de référence : info_seq-covid.txt").place(relx=0.05, rely=0.20, anchor="nw")
    titleTable1 = tk.Label(root, text="Tableau récapitulatif des informations sur les Coronavirus").place(relx=0.05, rely=0.27, anchor="nw")

    win = App(root)
    win.place(anchor="center", relx=0.5, rely=0.6)
    root.mainloop()