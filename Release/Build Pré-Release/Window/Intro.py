import tkinter as tk
from tkinter import messagebox

isClosed = True # On défini isClosed ; Cette variable permet de savoir si la fenêtre est fermée par l'utilisateur ou par un bouton

def DisplayIntro():
    #Définition de la fenêtre
    intro = tk.Tk()
    intro.geometry("500x250")
    intro.title("Corona Wrapper")
    intro.resizable(False, False); #Règle Resizable définie sur False => Limite les erreurs d'affichages car labels statiques
    intro.eval('tk::PlaceWindow . center')
    
    #Définition des Label
    firstTitle = tk.Label(intro, text="Richez Elie\nTavoillot Antoine\nSaidi Adel").place(relx = 0.02,rely = 0.95,anchor ='sw')
    year = tk.Label(intro, text="Université de Montpellier, 2022").place(relx = 0.98,rely = 0.95,anchor ='se')
    title = tk.Label(intro, text="Corona Wrapper", font=("Arial", 25)).place(relx = 0.98,rely = 0.05,anchor ='ne')

    #Définition du MenuBoutton pour la séléction de Preset
    startButton = tk.Button(intro, text="Débuter le Processus Automatique", relief="raised", command=lambda:[changeQuitDef(), intro.destroy()]).place(relx = 0.3,rely = 0.35, anchor ='center')
    creditButton = tk.Button(intro, text="Crédit", relief="raised", command=credit).place(relx = 0.13,rely = 0.47, anchor ='center')

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
    msgBox = messagebox.showinfo(title="Signature RSA", message="-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA256\n\nSignature RSA, pour le projet CoronaScrapper\nRichez Elie, Saidi Adel et Antoine Tavoillot,\nUniversité de Montpellier, Licence L1 d’informatique groupe B,\nEditée le 7 Novembre 2022\nEmpreinte de clé publique : 680A 1D42 AF6A 6313 A7B1 814D F527 954F 3054 4C37\n-----BEGIN PGP SIGNATURE-----\n\niQIzBAEBCAAdFiEEaAodQq9qYxOnsYFN9SeVTzBUTDcFAmNo0ZAACgkQ9SeVTzBU\nTDeNAxAAr6/dNsLeGhSwOktquW3n43E/LDJi5aIV9g3CPGG6N1QP9xkXVLEQP0+/\neM2empwi015N66eD4ZrX+xEGRI+HIPSyXOKTCUFfWKN/mb8tvLtECJPKn8dk+dH+\nTFSpqwkb7qkObqlbj4Z4mxp4HVTJlZTlYp309rWg2wFrRbSLOGekCBAP51Oa7T6f\nnZl+P3fQOBP9GMYUCSCsWNsqk53oV4YZM6O2qfJY84BMvJ8dTJ9YpiJfTTwwkzxZ\n49ZJbLyjSiR+nvOrfi0gqgPIYTbREhzo2KvqhMmnxHPYJUKoBGtsqfqiv1GHQoaL\nKnPlITepGnK7IBUVPs2nI833JimcNxdvIIsEdJ0WZ9QZIJx9mj0XpiBni7034mIG\n4dNwD/DrEqD93EfOnJsZBdsKYmLH4rkvd5QGW36DdiqVjdkUbvK1NtJjWftXjFzW\nqO1aGXHdTN3HwP1tzp8UnyYaj0Ym2UeN4zh4KHE0UzPwJ4BMjJkcoKwRi7BcDWRo\nTKgfohcr7TCNp6WkU6wemDJ3B0eRmkrABHDAaFDhea46zlPrv7nHTBvG0dY38dqd\nkgECk6Pp+LQSP+VAzKWDniAFHAd/azZcGWRJWijSropP6XU6KJ8ogOnjG9xOhryu\n9WZ09B8/I5oefYEQ4Y0qYefHLAMI8WkU/YG9MP9h0DciUnDhbZA=\n=fBVz\n-----END PGP SIGNATURE-----\n")

def credit():
    msgBox = messagebox.showinfo(title="Crédit", message="Licence Informatique - Groupe B\nTavoillot Antoine\nRichez Elie\nSaidi Adel\nUniversité de Montpellier (2022)")
