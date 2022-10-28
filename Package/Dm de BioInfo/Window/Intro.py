import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

def infoBox():
    msgBox = messagebox.showinfo(title="Contenu du Preset 1", message="Le Preset contient :\n-SARS-CoV-2\n-SARSr-CoV RaTG13\n-SARS-Cov MP789")

isClosed = True

def DisplayIntro():
    #Définition de la fenêtre
    intro = tk.Tk()
    intro.geometry("500x250")
    intro.title("Corona Scrapper - Alpha 0.1")
    intro.resizable(False, False); #Règle Resizable définie sur False => Limite les erreurs d'affichages car label dynamique
    intro.eval('tk::PlaceWindow . center')

    #Définition des Label
    firstTitle = tk.Label(intro, text="Ritchez Elie\nTavoillot Antoine\nSahidi Adell").place(relx = 0.98,rely = 0.95,anchor ='se')
    year = tk.Label(intro, text="Université de Montpellier, 2022").place(relx = 0.02,rely = 0.95,anchor ='sw')
    title = tk.Label(intro, text="Choisissez votre Preset et cliquez sur continuer : ").place(relx = 0.02,rely = 0.055,anchor ='w')


    #Définition du MenuBoutton pour la séléction de Preset
    mb = tk.Button(intro, text="Preset", relief="raised", command=lambda:[changeQuitDef(), intro.destroy()]).place(relx = 0.78,rely = 0.06, anchor ='e')

    #Définition du Bouton d'aide concernant les Preset
    icon = Image.open("Resources/InterrogationIcon.png") #Import de l'icone
    icon = icon.resize((15,15))#Modification de la taille de l'Icône
    usableIcon = ImageTk.PhotoImage(icon)
    btn = tk.Button(intro, text ='open image', image=usableIcon, borderwidth=0, command=infoBox).place(relx = 0.98,rely = 0.06, anchor ='e')#Display du Bouton

    #Menu
    menubar = tk.Menu(intro)
    intro.config(menu=menubar)
    menufichier = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Fichier", menu=menufichier)
    menufichier.add_command(label = "Importer un fichier")
    menufichier.add_command(label = "Exporter au format txt")
    menufichier.add_separator()
    menufichier.add_command(label = "Quitter", command=quit)

    menuprofile = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label = "Utilisateur", menu=menuprofile)
    menuprofile.add_command(label="Preset Covid")
    menuprofile.add_command(label="Preset 2")
    menuprofile.add_command(label="Preset 3")

    #Display de la fenêtre
    intro.mainloop()
    global isClosed
    return isClosed

def changeQuitDef():
    global isClosed
    isClosed = False