import os
import tkinter as tk
from tkinter import messagebox

def Composite():
    if PingTestMessageBox() == "Error Connexion Status":
        return 0
    else:
        return 1

def PingTestMessageBox():
    result = PingCheck()
    if result == 0:
        msgBox = messagebox.showerror(title="Connexion Error", message="Aucune connexion réseau détectée ; Le scrapper ne peut fonctionner")
        return "Error Connexion Status"
    return "Connexion OK"

def PingCheck():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        pingstatus = 1
    else:
        pingstatus = 0

    return pingstatus

