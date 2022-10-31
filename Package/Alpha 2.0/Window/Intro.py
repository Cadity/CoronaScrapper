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
    intro.title("Corona Scrapper - Alpha 1")
    intro.resizable(False, False); #Règle Resizable définie sur False => Limite les erreurs d'affichages car label dynamique
    intro.eval('tk::PlaceWindow . center')
    
    #Définition des Label
    firstTitle = tk.Label(intro, text="Ritchez Elie\nTavoillot Antoine\nSaidi Adell").place(relx = 0.02,rely = 0.95,anchor ='sw')
    year = tk.Label(intro, text="Université de Montpellier, 2022").place(relx = 0.98,rely = 0.95,anchor ='se')
    title = tk.Label(intro, text="Corona Wrapper", font=("Arial", 25)).place(relx = 0.98,rely = 0.05,anchor ='ne')


    #Définition du MenuBoutton pour la séléction de Preset
    startButton = tk.Button(intro, text="Débuter le Processus Automatique", relief="raised", command=lambda:[changeQuitDef(), intro.destroy()]).place(relx = 0.6,rely = 0.5, anchor ='e')

    #Définition du Bouton d'aide concernant les Preset
    icon = Image.open("Resources/InterrogationIcon.png") #Import de l'icone
    icon = icon.resize((15,15))#Modification de la taille de l'Icône
    usableIcon = ImageTk.PhotoImage(icon)
    btn = tk.Button(intro, text ='open image', image=usableIcon, borderwidth=0, command=infoBox).place(relx = 0.05,rely = 0.06, anchor ='w')#Display du Bouton

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

    menuhelp = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label = "Aide", menu=menuhelp)
    menuhelp.add_command(label="Signature RSA du Logiciel", command=RSASign)
    menuhelp.add_command(label="Version du Logiciel", command=infoVersion)

    #Display de la fenêtre
    intro.mainloop()
    global isClosed
    return isClosed

def changeQuitDef():
    global isClosed
    isClosed = False

def infoVersion():
    msgBox = messagebox.showinfo(title="Version du Logiciel", message="Alpha 1.0 (Build 1)")

def RSASign():
    msgBox = messagebox.showinfo(title="Version du Logiciel", message="-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA256\n\nSignature RSA du Document,\nProduit le 28 Octobre 2022,\n\nEmpreinte de Clé : 268C C768 48B9 A579 3271 9C67 0794 7D80 F311 C3F8\n-----BEGIN PGP SIGNATURE-----\n\niQIzBAEBCAAdFiEEJozHaEi5pXkycZxnB5R9gPMRw/gFAmNbq8wACgkQB5R9gPMR\nw/ivXhAAuftRpgdvU6jaO25taqFGO+5IR1z6uyUXXTmzUEMqgWaJ2uz0sHDJO0mk\nhLztjAexl0EhFQ/ABJ55V4H+7cPEQL7nooSuMg9axtmost80muweJNzp5Y9fs3Ua\nU9g43oeUdKAGlOPTuWC1lwwWWypTprW5WyNyGYuZTzGOKHgTY+VEbhFmVfGOR0g0\nh4lVeLHYR8QFgJLIvDcATpED4xdVEJjeS9y6281zW8cGItXmYsvfbUW4WTdYbB9P\nsRON8UXkgh35vlKiMPhqBkUOt05QrlrodjpOPbWpuOpnA6+JsbMXyM5ihH6ozrrz\niNuvvTXjh5PbZkd02d+RYIYIMHq2RAPKk6KVtAIPYkmEydgjqGKf9SBKO3tJL97R\nWlJPXw2k9damwbgpYxwCzI93E8Soe9VY+pqvm/J7NxyZi1ACJrqmj97cGPWsN81L\nR6MW3RO7AsH8ybc7NZ7xwIIqITSfKcRVzWKiy51Vwh0X8IqhfhoT9j0Z2BidDLU6\naGZIyU+y51TQ1ux60emawEUGbqJgFxLOATwrE3b3wedMvC9MIbCToTOu551QoWCN\nAE56cu6zdJyhcMrVFtUWMmXOF7N4fa2gBWnohvLMPe0O47+6GeROrz0exafHZ6l7\netAsdceqllGRtgD4WNLvrPmbHcK9zPYIjhHQSSniTWy2+dvJQcw=\n=izEP\n-----END PGP SIGNATURE-----\n")