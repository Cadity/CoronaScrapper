import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from Window.Graph import DisplayGraph
from shutil import *
from Logs import MakeLogs
from Scrapper.WriteData import Etapes, Main

global dataList
dataList = list()


class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.table = TableCnv(self, width = 1000, height = 250)
        self.table.pack()

        global dataList
        proteinList = dataList[1]

        def changeTableCurrent(event):
            selectedGen = listeCombo.get()
            msgBox = messagebox.showinfo(title="Table à jour", message="Le tableau à correctement été mis à jour avec le gène " + selectedGen)
            MakeLogs("Le gène, " + selectedGen.split("Protéine ")[1] + " à été sélectionné et les fichiers mis à jours")

            self.table.currentGene = selectedGen

            self.table.defaultTab()

        def Quit():
            DisplayGraph()

        btn = tk.Button(self, text="Table des virus", command=self.table.defaultTab)
        btn.pack()

        btn = tk.Button(self, text="Graphique", command=lambda:[self.quit(), Quit()])
        btn.place(relx=0.85, rely=0.85)

        btn = tk.Button(self, text="Table des gènes", command=self.table.genTable)
        btn.pack()

        btn = tk.Button(self, text="Comparaison des nucléotides", command=self.table.nucCompare)
        btn.place(relx=0.05, rely=0.9)

        listeCombo = Combobox(self, values=proteinList)
        listeCombo.current(1)
        listeCombo.place(relx=0.05, rely=0.8)
        listeCombo.bind('<<ComboboxSelected>>', changeTableCurrent)

class TableCnv(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.currentGene = "Protéine S"
        self.resultList = Main.GetOneGeneData(self.currentGene)
        self.dataList = self.resultList[0]

        self.errorList = self.resultList[1]

        self.labelText = tk.StringVar()
        self.labelText.set("")
        self.protTitle = tk.Label(self, textvariable=self.labelText).place(relx=0.05, rely=0.05, anchor="nw")

        self.tableau = Treeview(self, columns=('','virus1', 'virus2', 'virus3'))
        self.tableau.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.9)
        MakeLogs("Les données ont été parfaitement chargées !")
        self.defaultTab()
        
    def defaultTab(self):
        self.clear()

        self.labelText.set("Analyse des virus : ")

        self.tableau.heading('virus1', text=self.dataList[1][0])
        self.tableau.heading('virus2', text=self.dataList[1][1])
        self.tableau.heading('virus3', text=self.dataList[1][2])
        self.tableau['show'] = 'headings'
       
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
        print(self.currentGene)
        try:
            self.resultList = Etapes.Etape_E(self.currentGene.split("Protéine ")[1])
            self.labelText.set("Taux de conservation de la protéine " + self.currentGene + " : " + str(self.resultList[4]) + " %, pour la chauve souris, " + str(self.resultList[5]) + " %, pour le Pangolin")

            self.tableau.heading('virus1', text="Homme")
            self.tableau.heading('virus2', text="Chauve-Souris")
            self.tableau.heading('virus3', text="Pangolin")

            for a in range(len(self.resultList[0])):
                self.tableau.insert('', 'end', values=(self.resultList[0][a], self.resultList[1][a], self.resultList[2][a], self.resultList[3][a]))
        except Exception as e:
            analysisError = messagebox.showinfo(title="Erreur d'acquisition des informations sur le gène", message="Le gène " + self.currentGene + " semble apparaître sous plusieurs orthographes différentes et ne peut pas être analysé")
            MakeLogs("Levée d'exception fatale\n{\n\tDescription : " + str(e) + "\n\tRésolution : Aucune résolution n'a été prévue par CoronaWrapper\n}")
            print(e)
            self.defaultTab()
              
def Display(data):
    global dataList
    dataList = data
    # Window Settings
    root = tk.Tk()
    root.geometry("1000x500")
    root.title("Résultat d'analyse du fichier GenBank")
    root.resizable(False, False)


    # Label
    firstTitle = tk.Label(root, text="Résultat d'analyse du fichier GenBank : ").place(relx=0.02, rely=0.02, anchor="nw")
    #seqNumber = tk.Label(root, text="Nombre de séquences : " + str(dataList[0])).place(relx=0.05, rely=0.12, anchor="nw")
    genBankPath = tk.Label(root, text="Fichier de référence GenBank : seq_covid.gb").place(relx=0.05, rely=0.16, anchor="nw")
    pathDoc = tk.Label(root, text="Emplacement du document de référence : info_seq-covid.txt").place(relx=0.05, rely=0.20, anchor="nw")
    titleTable1 = tk.Label(root, text="Tableau récapitulatif des informations sur les Coronavirus").place(relx=0.05, rely=0.27, anchor="nw")

    try:
        #Menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        menufichier = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Graphique", menu=menufichier)
        menufichier.add_command(label="Ouvrir la fenêtre des graphiques")
    except:
        MakeLogs("Exception fatale\n{\n\tUne exception s'est produite lors de l'utilisation de la barre de menu\n}")

    # Photo du Coronavirus
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