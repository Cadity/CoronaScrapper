from os import *
from tkinter import messagebox
from Bio import Entrez
from Bio import SeqIO
import time
from os import path
from Logs import MakeLogs

def PingCheck():
    hostname = "google.com" # Hostname
    response = system("ping -c 1 " + hostname) # Réponse de la connexion à l'hôte
    if response == 0: # Si la réponse est 0
        pingstatus = 1 # On retourne à un pingStatus de 1
        MakeLogs("La connexion avec un serveur de google à été établie avec succès")
    else:
        msgBox = messagebox.showerror(title="Erreur de connexion au serveur", message="La tentative de connexion au serveur à échouée")
        pingstatus = 0

    return pingstatus # On retourne le status pour communiquer la réussite ou non de la connexion

def GetData():
    filePath = "Fichiers externes"

    if path.exists(filePath + "/seq_covid.gb") == True:
        return

    start_time = time.time()
    Entrez.email = "antoinetavoillot@gmail.com" # Email pour la requête
    MakeLogs("Connexion au serveur de la banque du NCBI")
    MakeLogs("Connexion réussie")

    # Ensemble des requêtes vers les pages du NCBI sur la base de données "Nucléotide" et obtention du résultat au format genbank
    humanCovReq = Entrez.esearch(db="nucleotide", term="SARS-COV 2[orgn] AND srcdb_refseq [SPIKE]", rettype="gb") # Requête pour le SARS-Cov 2 humain
    batCovReq = Entrez.esearch(db="nucleotide", term="Bat coronavirus RaTG13[Organism] OR Bat Coronavirus RATG13[All Fields]", rettype="gb") # Requête pour le Coronavirus RaTG13 de la Chauve-Souris (Bat)
    pangCovReq = Entrez.esearch(db="nucleotide", term="MT121216", rettype="gb") # Requête pour le Coronavirus MP789 Du Pangolin

    # Lecture des fichiers XML obtenus
    humanCovRes = Entrez.read(humanCovReq)
    ratCovRes = Entrez.read(batCovReq)
    pangCovRes = Entrez.read(pangCovReq)
    MakeLogs("Les fichiers XML de la banque du NCBI ont été obtenus avec succès")

    # Création de la liste d'identifiant NCBI des virus
    idList = list()
    idList.append(humanCovRes["IdList"][0]) # Identifiant du Sars-Cov 2 Humain => 1798174254
    idList.append(ratCovRes["IdList"][0]) # Identifiant du Bat Coronavirus RaTG13 => 1916859392
    idList.append(pangCovRes["IdList"][0]) # Identifiant du Coronavirus du Pangolin MT121216 => 1817977257

    MakeLogs("Renouvellement de la requête vers la banque du NCBI")

    # Requête vers le NCBI avec la liste des identifiants
    fullSeq = Entrez.efetch(db="nucleotide", id=idList, rettype="gb")
    mesSeq = SeqIO.parse(fullSeq, "gb") # Parse des résultats obtenus => Type SeqIO

    
    SeqIO.write(mesSeq, filePath + "/seq_covid.gb", "genbank") # Ecriture des séqueces au formant GenBank dans le fichier seq_covid.gb
    requestTime = round((time.time() - start_time), 2)
    MakeLogs("Génération du fichier GenBank réussi en " + str(requestTime) + " secondes")
    return True

def GetGenSeqGB(gene, listID):
    Entrez.email = "antoinetavoillot@gmail.com" # Email pour la requête

    # Ensemble des requêtes vers les pages du NCBI sur la base de données "Nucléotide" et obtention du résultat au format genbank
    humanGeneReq = Entrez.esearch(db="protein", term=listID[0], rettype="gb") # Requête pour le SARS-Cov 2 humain
    batGeneReq = Entrez.esearch(db="protein", term=listID[1], rettype="gb") # Requête pour le Coronavirus RaTG13 de la Chauve-Souris (Bat)
    pangGeneReq = Entrez.esearch(db="protein", term=listID[2], rettype="gb") # Requête pour le Coronavirus MP789 Du Pangolin

    # Lecture des fichiers XML obtenus
    humanCovRes = Entrez.read(humanGeneReq)
    ratCovRes = Entrez.read(batGeneReq)
    pangCovRes = Entrez.read(pangGeneReq)

    # Création de la liste d'identifiant NCBI des virus
    idList = list()
    idList.append(humanCovRes["IdList"][0]) # Identifiant du Sars-Cov 2 Humain => 1798174254
    idList.append(ratCovRes["IdList"][0]) # Identifiant du Bat Coronavirus RaTG13 => 1916859392
    idList.append(pangCovRes["IdList"][0]) # Identifiant du Coronavirus du Pangolin MT121216 => 1817977257

    # Requête vers le NCBI avec la liste des identifiants
    fullSeq = Entrez.efetch(db="protein", id=idList, rettype="gb")
    mesSeq = SeqIO.parse(fullSeq, "gb") # Parse des résultats obtenus => Type SeqIO

    repPath = "Fichiers externes/Protéines/Protéine " + gene + "/"

    SeqIO.write(mesSeq, repPath  + gene + ".gb", "genbank") # Ecriture des séqueces au formant GenBank dans le fichier seq_covid.gb