from Window.Intro import DisplayIntro
from Window.MainWindow import Display
from Coronavirus.PingTest import check_ping

result = DisplayIntro() #On affiche la fenêtre d'introduction

if result == False: #Si la règle isClosed est fausse (donc que le fenêtre n'est pas fermé soit avec le clavier soit avec la "Croix")
    Display() #On affiche la fenêtre principal

