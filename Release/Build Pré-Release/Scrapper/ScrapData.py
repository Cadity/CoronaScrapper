import os
from tkinter import messagebox
from Bio import Entrez
from Bio import SeqIO
import time

def PingCheck():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        pingstatus = 1
    else:
        msgBox = messagebox.showerror(title="Erreur de connexion au serveur", message="La tentative de connexion au serveur à échouée")
        pingstatus = 0

    return pingstatus


def GetData():
    start_time = time.time()
    Entrez.email = "antoinetavoillot@gmail.com" # Email pour la requête

    # Ensemble des requêtes vers les pages du NCBI sur la base de données "Nucléotide" et obtention du résultat au format genbank
    humanCovReq = Entrez.esearch(db="nucleotide", term="SARS-COV 2[orgn] AND srcdb_refseq [SPIKE]", rettype="gb") # Requête pour le SARS-Cov 2 humain
    batCovReq = Entrez.esearch(db="nucleotide", term="Bat coronavirus RaTG13[Organism] OR Bat Coronavirus RATG13[All Fields]", rettype="gb") # Requête pour le Coronavirus RaTG13 de la Chauve-Souris (Bat)
    pangCovReq = Entrez.esearch(db="nucleotide", term="MT121216", rettype="gb") # Requête pour le Coronavirus MP789 Du Pangolin

    # Lecture des fichiers XML obtenus
    humanCovRes = Entrez.read(humanCovReq)
    ratCovRes = Entrez.read(batCovReq)
    pangCovRes = Entrez.read(pangCovReq)

    # Création de la liste d'identifiant NCBI des virus
    idList = list()
    idList.append(humanCovRes["IdList"][0]) # Identifiant du Sars-Cov 2 Humain => 1798174254
    idList.append(ratCovRes["IdList"][0]) # Identifiant du Bat Coronavirus RaTG13 => 1916859392
    idList.append(pangCovRes["IdList"][0]) # Identifiant du Coronavirus du Pangolin MT121216 => 1817977257

    # Requête vers le NCBI avec la liste des identifiants
    fullSeq = Entrez.efetch(db="nucleotide", id=idList, rettype="gb")
    mesSeq = SeqIO.parse(fullSeq, "gb") # Parse des résultats obtenus => Type SeqIO

    SeqIO.write(mesSeq, "seq_covid.gb", "genbank") # Ecriture des séqueces au formant GenBank dans le fichier seq_covid.gb
    requestTime = round((time.time() - start_time))
    msgBox = messagebox.showinfo(title="Délai de réponse", message="Réponses obtenues en " + str(requestTime) + " secondes")
    return True