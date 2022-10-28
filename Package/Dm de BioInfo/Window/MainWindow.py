import tkinter as tk

def Display():
    #Définition de la fenêtre
    root = tk.Tk()
    root.geometry("700x500")
    root.title("DM de Bio_Informatique")
    root.resizable(False, False)

    #Menu
    menubar = tk.Menu(root);
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
    firstTitle = tk.Label(root, text="Sélection du profil utilisateur :");
    firstTitle.place(x = 10, y = 10)

    #Display de la fenêtre
    root.mainloop()