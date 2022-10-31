from Window.Intro import DisplayIntro
from Window.MainWindow import Display
from Scrapper.ScrapData import Composite
from tkinter import filedialog

result = DisplayIntro() #On affiche la fenêtre d'introduction

if result == False: #Si la règle isClosed est fausse (donc que le fenêtre n'est pas fermé soit avec le clavier soit avec la "Croix")
    if Composite() == 0:
         quit()
else:
    quit()

selectedPath = filedialog.askdirectory(title="Dialog box", initialdir="/")
print(selectedPath)

Display()

