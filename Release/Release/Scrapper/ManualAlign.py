from Bio import SeqIO 
import numpy as np

repPath = "Fichiers externes/Protéines"

class Alignement():
    def AlignLoop(Seq1, Seq2):
        # Définition colonne et ligne de la matrice
        n = len(Seq1)
        m = len(Seq2)
        matrice = np.zeros((n + 1, m + 1)) # Création d'une matrice constituée uniquement de 0

        # Remplissage de la matrice (Colonne 0 et ligne 0)
        for a in range(n + 1): 
            matrice[a][0] = -a
        for x in range(m + 1):
            matrice[0][x] = -x
        
        # Boucle de remplissage de la matrice avec la comparaison de séquence
        # On démarre de 1 pour exclure la ligne et la colonne 0
        for a in range(1, n + 1):
            for x in range(1, m + 1):
                if Seq1[a-1] != Seq2[x - 1]:
                    resMatrice = -1 # Variable de complétion de la matrice (2 si la Seq[a-1] != Seq[x-1])
                else:
                    resMatrice = 2 # Variable de complétion de la matrice (-1 comme Seq[a-1] == Seq[x-1])
                # Complétion de la matrice pour toutes les cases
                matrice[a][x] = max(matrice[a - 1][x - 1] + resMatrice, matrice[a - 1][x] - 1, matrice[a][x - 1] - 1)

        # Définition de variable
        resSeq1 = "" # Variable de résultat pour la séquence 1
        resSeq2 = "" # Variable de résultat pour la séquence 2

        a = n # Création d'une var pour ne pas modifier n
        x = m # Création d'une var pour ne pas modifier m

        while a > 0 or x > 0: # Boucle principale
        # on recalcule la variable de complétion
            if Seq1[a - 1] != Seq2[x - 1]:
                    resMatrice = - 1
            else:
                resMatrice = 2

            # Création des trois paramètres : Depuis une case, soit on va à gauche (on remonte la matrice), soit on se déplace dans la colonne,
            # Soit on se déplace en diagonale

            upCase = matrice[a][x - 1] - 1
            diagCase = matrice[a - 1][ x -1] + resMatrice
            leftCase = matrice[a - 1][x] - 1

            # Obtention du max de la matrice sur la colonne de gauche, colonne ou diagonale correspondante
            maxMatrice = max(leftCase, diagCase, upCase)

            if maxMatrice == diagCase: # Si le max de la matrice est égale à la diagonale, on se déplace sur la diagonale
                resSeq1 += Seq1[a - 1]
                resSeq2 += Seq2[x - 1]
                a -= 1
                x -= 1
            elif maxMatrice == leftCase: # Si le max est situé à gauche, on se déplace sur la case à gauche
                resSeq1 += Seq1[a - 1]
                resSeq2 += "-"
                a -= 1
            else:
                resSeq1 += "-" # Sinon, on se déplace sur la colonne
                resSeq2 += Seq2[a - 1]
                x -= 1

        resList = list()
        # La liste contient des séquences inversés ; Donc on les réinverses
        resList.append(resSeq1[::-1])
        resList.append(resSeq2[::-1])
        return resList

    def Main(gene): # Fonction contenant la boucle d'écriture 
        genePath = repPath + "/Protéine " + gene # Répertoire du gène en cours

        # Définition des listes de données        
        SeqList = list() # Liste de séquences
        DescriptionList = list() # Liste des description inclues dans le fichier fasta

        with open(genePath + "/" + gene + ".fasta", "r") as fastaFile: # Ouverture du fichier fasta
            for Seq in SeqIO.parse(fastaFile, "fasta"): # Pour toutes les séquences trouvées dans le fichier...
                SeqList.append(Seq.seq) # On récupère la séquence
                DescriptionList.append(Seq.description) # On récupère la description
        
        with open(genePath + "/manual-align-" + gene + ".fasta", "w") as alignedFile: # On créé le fichier /manual-align-gene au format fasta
            for a in range(len(SeqList)): # A prends l'occurence du nombre d'élément dans SeqList
                for x in range(a+1, len(SeqList)): # x prends l'occurence entre a + 1 et le nombre d'élement 
                    resList = list() # Définition de la liste de résultat
                    resList = Alignement.AlignLoop(SeqList[a], SeqList[x]) # Qui prend le résultat de l'alignement
                    # Ecriture dans le fichier fasta (Ecriture manuelle, plus simplifiée qu'avec un objet SeqIO)
                    alignedFile.write(">" + DescriptionList[a] + "\n" + resList[0] + "\n")
                    alignedFile.write(">" + DescriptionList[x] + "\n" + resList[1] + "\n\n")


