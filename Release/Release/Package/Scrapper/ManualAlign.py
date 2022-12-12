# Code pour la matrice
from Bio import SeqIO 
from Bio.SeqUtils import GC # Module de calcul du taux de GC
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Align.Applications import MafftCommandline
import os
from os import path
from Scrapper.ScrapData import GetGenSeqGB, GetData
from Logs import MakeLogs
import numpy as np

# Variable globale ; n et m ne sont jamais modifiés mais empruntés
global n, m
global matrice # La matrice est définie en global car elle pourra 

def RedefineVar():
    global n, m
    n = 0
    m = 0
    global matrice


class MatriceTransform(): # Classe de création de la matrice

    def CreateInitialMatrice(seqlist): # Ici on implante une matrice de taille n,m de zéros
        global n, m, matrice
        n = len(seqlist[0]) + 1 # n
        m = len(seqlist[1]) + 1 # m
        matrice = np.zeros((n,m)) # Définition de la matrice de zéros
        
        for a in range(n): # Boucle pour remplir la ligne 0
            matrice[a,0] = -a
        for x in range(m): # Boucle pour remplir la colonne 0
            matrice[0,x] = -x

    def GetWrittedMatrice(seqlist): # Fonction pour obtenir une matrice complète
        global matrice, m, n 
        
        for x in range(len(seqlist[0])): # Ici, x prends une valeur dans le range de la plus petite séquence
            if seqlist[0][x] == seqlist[1][x]: # Comparaison des valeurs
                matrice[x + 1,x + 1] = matrice[x, x] + 2 # On ajoute deux dans la case x,x par rapport à la case x-1, x - 1

            for a in range(0, m - x): # Boucle de remplissage de la ligne
                matrice[x,x + a] = matrice[x,x] - a

            for b in range(0, n - x): # Boucle de remplissage de la colonne
                matrice[x + b,x] = matrice[x,x] - b

        matrice[0,0] = 0 # On évite les erreurs en redéfinissant le point 0,0 à 0

class ReadMatrice(): # Classe de lecture de la matrice
    def Read(seqList): # Fonction principale de la classe
        global matrice, m, n
        alnSeq1 = ""
        alnSeq2 = ""

        # Maintenant on recherche dans la matrice
        pow2 = 2
        for x in range(n):
            if matrice[x,x] % 2 == 0 and matrice[x,x] > 0:
                alnSeq1 = alnSeq1 + seqList[0][x - 1]
                alnSeq2 = alnSeq2 + seqList[1][x - 1]
            else:
                if x != 0:
                    alnSeq1 = alnSeq1 + seqList[0][x - 1]
                    alnSeq2 = alnSeq2 + "-"
                    
        resultList = list()
        resultList.append(alnSeq1)
        resultList.append(alnSeq2)

        return resultList

class MainAlign():

    def lenTest(seq1, seq2):
        # Cette fonction permet de définir quelle est la séquence la plus grande
        # afin de créer une matrice de taille n, m

        seqList = list() # Cette liste contient la sequence la plus petite en 0 et la séquence la plus grande en 1

        if len(seq1) < len(seq2):
            seqList.append(seq1)
            seqList.append(seq2)
        else:
            seqList.append(seq2)
            seqList.append(seq1)

        return seqList

    def Main(seq1, seq2): # Fonction qui renvoie l'alignement de la séquence
        RedefineVar()
        seqList = MainAlign.lenTest(seq1, seq2)
        global matrice
        MatriceTransform.CreateInitialMatrice(seqList)
        MatriceTransform.GetWrittedMatrice(seqList)
        newSeqList = ReadMatrice.Read(seqList)

        return newSeqList

def GetSeq(seq1, seq2):
    return MainAlign.Main(seq1, seq2)
        
# Séquence pour test