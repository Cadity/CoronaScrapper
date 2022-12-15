# Fichier de lecture et d'écriture

from Bio import SeqIO 
from Bio.SeqUtils import GC # Module de calcul du taux de GC
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Align.Applications import MafftCommandline
from Scrapper.ManualAlign import Alignement
import os
from os import path
from Scrapper.ScrapData import GetGenSeqGB, GetData
from Logs import MakeLogs, Event
import time

# Déclaration de variables de répertoire
repPath = "Fichiers externes/Protéines"
filePath = "Fichiers externes"

global writeRule # Déclaration de la règle d'écriture (booléen, True signifie que les fichiers seront écris)

class Main():
    def EntryPoint(): # Fonction de départ 
        finalList = list() # Définition de la liste de données qui sera retournée
        geneList = list() # Définition de la liste de gènes
        global result_Etape_B

        External.CheckPath() # On vérifie les fichiers
        External.StartLog() # Ecriture du log de début de l'opération
        start_operation_time = time.time() # Timer pour l'opération
        GetData()

        result_Etape_B = Etapes.Etape_B() # On stocke les données récupérées de l'étape B
        finalList.append(result_Etape_B) # On l'ajoute à la liste finale
        geneList = External.GetGenList(result_Etape_B[8]) # On obtiens la liste de gènes
        finalList.append(geneList)
        finalList.append(Main.GeneLoop(geneList))

        end_operation_time = round((time.time() - start_operation_time), 2)

        External.EndLog(end_operation_time)

        return finalList
        
    def GeneLoop(genList): # Fonction d'écriture et d'analyse pour l'ensemble des gènes de la liste
        data = list()
        for gene in genList:
            geneTime = time.time() # Timer pour l'opération
            currentGene = gene.split("Protéine ")[1]
            genePath = repPath + "/" + gene
            if path.exists(genePath) == False:
                os.mkdir(genePath)
            Etapes.Etape_C(currentGene)
            result = Etapes.Etape_D(currentGene) # On récupère le resultat du bloc try sur MAFFT
            data.append(Etapes.Etape_E(currentGene))
            Etapes.Etape_I(currentGene, result_Etape_B)
            Align.WriteAlign(currentGene)
            endOpeTime = round((time.time() - geneTime), 2)
            External.GeneLog(result, gene, endOpeTime)
        
        return data

    def GetOneGeneData(gene):
        finalList = list()
        result_Etape_B = Etapes.Etape_B()
        finalList.append(result_Etape_B)

        geneList = External.GetGenList(result_Etape_B[8])
        finalList.append(geneList)

        data = list()
        currentGene = gene.split("Protéine ")[1]
        genePath = repPath + "/" + gene
        if path.exists(genePath) == False:
                os.mkdir(genePath)
        Etapes.Etape_D(currentGene)
        data.append(result_Etape_B)
        data.append(Etapes.Etape_E(currentGene))
        Etapes.Etape_I(currentGene, result_Etape_B)

        finalList.append(data)

        return finalList

class External(): # Classe de fonction externe

    def CheckPath(): # Vérification de l'existance du répertoire Protéines
        global writeRule
        if path.exists(filePath + "/Protéines") == False:
            os.mkdir(filePath + "/Protéines")
            writeRule = True # Et on autorise l'écriture de fichier
        else:
            writeRule = False # Sinon on interdit pour éviter de réécrire constamment les fichiers

    def StartLog():
        global writeRule
        print(writeRule)

        if writeRule == True: # Implémentation du log de début de l'opération
            Event("L'opération d'écriture et d'analyse des fichiers à débutée")
        else:
            Event("L'opération d'analyse des fichiers à débutée")

    def EndLog(time):
        global writeRule
        if writeRule == True: # Implémentation du log de début de l'opération
            Event("L'opération d'écriture et d'analyse des fichiers s'est parfaitement terminée en " + str(time))
        else:
            Event("L'opération d'analyse des fichiers s'est parfaitement terminée en " + str(time))

    def GeneLog(result, gene, time):
        global writeRule
        var = ""
        if writeRule == True:
            var = "d'écriture et d'analyse"
        else:
            var = "d'analyse"

        text = "Opération " + var + " du gène " + gene + "\n{" + "\t- Durée : " + str(time) + "\n"

        if result != 0:
            text = text + "\t- Status : Succès de l'opération" + "\n\t- Commentaire : Aucune erreur detéctée"
        else:
            text = text + "\t- Status : Echec de l'opération" + "\n\t- Commentaire : Le gène " + gene + " n'est pas analysable"

        text = text + "\n}\n"

        MakeLogs(text)

    def GetGenList(allGenList): # Fonction permettant d'obtenir les gènes compris dans les trois génomes

        tempGenList = list() # Création d'une liste temporaire
        finalGenList = list() # Création de la liste finale

        for gene in allGenList: # On créé une boucle ou a prends une occurence de la totalité des gènes
            if(allGenList.count(gene) == 3): # On regarde si a est trois fois dans la liste
                if gene not in tempGenList: # On regarde si a est dans la liste temporaire ou non
                    gen = gene.upper() # On élève le gène en majuscule
                    tempGenList.append(gene) # On l'ajoute dans la liste temporaire
                    finalGenList.append("Protéine " + gen) # On l'ajoute dans la liste finale
 
        return finalGenList # On retourne la liste des gènes

class Etapes():
    
    def Etape_B():
        ensSeq = SeqIO.parse(filePath + "/seq_covid.gb", "genbank") #Parse des trois séquences

        seqCount = 0 #Comptage du nombre de séquence

        #Définition des Listes
        listName = list() # Liste des noms des virus
        listHost = list() # Liste des hôtes
        listTaxonomieId = list() # Liste des identifiants taxonomiques
        listAccessionsId = list() # Liste des identifiants d'accessions
        listCreationDate = list() # Liste des dates de création
        listGeneNumber = list() # Liste des nombres de gènes pour chaque virus
        listGCRate = list() # Liste des taux de GC pour chaque virus
        geneList = list() # Liste des gènes
        locationStartList = list() # Liste des positions de départs
        locationEndList = list() # Liste des positions de fins
        idProteinList = list()
        newGeneList = list()

        for seq in ensSeq: # Début de la boucle for, Seq prend la définition d'une occurence de ensSeq à chaque itération
            mesSeqF = seq.features # Obtention des features de seq
            listName.append(seq.annotations["organism"]) # Obtention du nom du virus
            listAccessionsId.append(seq.id) # Obtention de l'identifiant d'accession du virus
            number = 0 # Initialisation de la variable nombre, comptant le nombre de gène
            seqCount = seqCount + 1 # Incrémentation de seqCount à chaque itération
            listGCRate.append(round(GC(seq.seq), 2)) # Obtention du taux de GC et application d'un arrondi à 2 décimales
            for i in mesSeqF: # Début d'une boucle for dans la recherche des features, i prends la définition d'une occurence de mesSeqF à chaque itéation
                if i.type == "source": # On recherche dans source
                    listHost.append(i.qualifiers["host"][0]) # Obtention du qualifiers hôte et inclusion dans la liste d'hôte
                    listTaxonomieId.append(i.qualifiers["db_xref"][0].split("taxon:")[1]) # Obtention de l'identifiant taxonomique et inclusion dans la liste d'identifiant taxonomique
                    listCreationDate.append(i.qualifiers["collection_date"][0]) # Obtention de la date de création et inclusion dans la liste de date de création
                if i.type == "gene": # On recherche dans gene
                    number = number + 1 # A chaque recherche dans gène, on incrémente number de 1
                    geneList.append(i.qualifiers["gene"][0].lower()) # Obtention du nom de gène et inclusion dans la liste de gène
                    locationStartList.append(i.location.start) # Obtention de la position de départ du gène actuel et inclusion dans la liste de position de départ
                    locationEndList.append(i.location.end) # Obtention de la position de fin du gène actuel et inclusion dans la liste de position de départ
                if i.type == "CDS":
                    newGeneList.append(i.qualifiers["gene"][0])
                    idProteinList.append(i.qualifiers["protein_id"][0])
                    #idProteinList.append(i.qualifiers["protein_id"][0])
            listGeneNumber.append(number) # Sortie de boucle et ajout de la variable number à la liste de nombre de gènes pour chaque virus

        # On définit une boucle while pour vérifier qu'un CDS n'a pas plusieurs fois le même identifiant
        countOccur = 0
        while countOccur < len(newGeneList) - 1:
            if newGeneList[countOccur] == newGeneList[countOccur + 1]:
                # Si c'est le cas, on supprime le dernier
                idProteinList[countOccur] = idProteinList[countOccur]
                idProteinList.pop(countOccur + 1)
            countOccur = countOccur + 1

        global writeRule
        if writeRule == True: # Si l'écriture dans un fichier est autorisée
            # Définition de finalText, string qui sera écrite dans info_seq_covid.txt
            finalText = "Informations complémentaires sur les Coronavirus :\n(Source : NCBI)\n\n"

            count = 0 
            # Boucle de rédaction de la string dans le fichier info_seq_covid.txt
            for a in range(seqCount): # Boucle for dans un range du nombre de virus trouvé (pas de dépassement d'index) a prenant la définition d'un entier ->
                finalText = finalText + listName[a] + "\n{\n" # Ecriture du nom
                finalText = finalText + "\tOrganisme : " + listHost[a] + "\n" # Ecriture de l'hôte
                finalText = finalText + "\tIdentifiant taxonomique : " + listTaxonomieId[a] + "\n" # Ecriture de l'identifiant taxonomique
                finalText = finalText + "\tNuméro d'accession de la donnée GenBank : " + str(listAccessionsId[a]) + "\n" # Ecriture du numéro d'accession de la donnée GenBank
                finalText = finalText + "\tDate de création de la donnée GenBank : " + listCreationDate[a] + "\n" # Ecriture de la date de création
                finalText = finalText + "\tNombre de gène : " + str(listGeneNumber[a]) + "\n" # Ecriture du nombre de gène
                finalText = finalText + "\tTaux de GC : " + str(listGCRate[a]) + " %" + "\n" # Ecriture du taux de GC
                finalText = finalText + "\tGènes et localisation des gènes : " + "\n\t{\n" # Ecriture du titre de la section "Gènes et localisation des gènes"
                # Boucle for ; x prend la valeur d'un entier entre count et count + liste de gène
                # On additionne ensuite count et le nombre de gène ; Count (nouvelle valeur) devient le point de départ de la prochaine execution
                # Cela permet d'éviter le dépassement d'index et de placer les bons gènes sur les bon virus
                for x in range(count, count + listGeneNumber[a]):
                    finalText = finalText + "\t\tGène " + geneList[x] + "\n\t\t{\n\t\t\tPosition de départ : " + str(locationStartList[x]) + "\n\t\t\tPosition de fin : " + str(locationEndList[x]) + "\n\t\t\tIdentifiant de la protéine : " + idProteinList[x] + "\n\t\t}\n" # Ecriture sur la même ligne du nom du gène et des positions
                count = count + listGeneNumber[a] # Addition de count et du nombre de gène -> Nouveau point de départ
                finalText = finalText + "\t}\n}\n\n" # Rédation de la fin de la section virus

            # Ecriture dans le fichier info_seq_covid.txt en mode "effacement" ("w")
            file = open(filePath + "/info_seq_covid.txt", "w")
            file.write(finalText)
            file.close()
            MakeLogs("Le fichier info_seq_covid.txt à été correctement généré")

        # Retour d'une liste de listes avec l'ensemble des données pour l'affichage sur la fenêtre principale
        fullDataList = list()
        fullDataList.append(seqCount)
        fullDataList.append(listName)
        fullDataList.append(listHost)
        fullDataList.append(listTaxonomieId)
        fullDataList.append(listAccessionsId)
        fullDataList.append(listCreationDate)
        fullDataList.append(listGeneNumber)
        fullDataList.append(listGCRate)
        fullDataList.append(geneList)
        fullDataList.append(idProteinList)
        fullDataList.append(locationStartList)
        fullDataList.append(locationEndList)

        MakeLogs("Les données en provenance du fichier seq_covid.gb ont été parfaitement récupérées")

        return fullDataList

    def Etape_C(gene):
        ensSeq = SeqIO.parse(filePath + "/seq_covid.gb", "genbank") #Parse des trois séquences

        listSeqRecord = list() # Définition de la liste des SeqRecord
        currentVirus = "" # Définition d'une variable currentVirus pour connaître le virus étudié à un instant T
        for seq in ensSeq: # Boucle for, seq prends la valeur de l'occurence de ensSeq à chaque itération
            currentVirus = seq.description # On attribue seq.description à currentVirus à chaque itération
            for i in seq.features: # Boucle for, on recherche dans les features de Seq
                if i.type == "CDS": # On affine la recherche ; uniquement le feature de type CDS
                    if i.qualifiers["gene"][0] == gene: # On affine la recherche ; uniquement si le gène actuel est S, pour "Spike"
                        listSeqRecord.append(SeqRecord(Seq(i.qualifiers["translation"][0]), id=i.qualifiers["protein_id"][0], name=i.qualifiers["gene"][0], description=currentVirus + ", " + i.qualifiers["product"][0])) # On rempli la liste de SeqRecord
        
        if len(listSeqRecord) == 0: # Si la liste de seqRecord à une longueur nulle
            return # On empêche l'écriture du fichier

        global writeRule 
        if writeRule == True: # Si l'écriture est autorisée
            SeqIO.write(listSeqRecord, repPath + "/Protéine " + gene + "/" + gene + ".fasta", "fasta") # On écris les SeqRecord dans le fichier spike.fasta au format fasta
        
        return listSeqRecord

    def Etape_D(gene):
        global writeRule
        if writeRule == True:
            return 2 # Code pour signifier que le fichier n'a pas besoin d'être écris

        try:
            from Bio.Align.Applications import MafftCommandline
            commande = MafftCommandline(input= repPath + "/Protéine " + gene + "/" + gene + ".fasta")
            myStdout, myStderr = commande()
            with open(repPath + "/Protéine " + gene + "/" + "aln-" + gene + ".fasta", 'w') as w:
                w.write(myStdout)
            return 1 # Le fichier à été parfaitement généré
        except:
            return 0 # Le fichier n'a pas pu être généré en raison d'une exception ; Cas d'ORF1AB

    def Etape_E(gene):

            try: # # On fait un try except pour attraper une exception si le fasta d'un gène n'existe pas
                ensSeq = SeqIO.parse(repPath + "/Protéine " + gene + "/" + "aln-" + gene + ".fasta", "fasta") # On obtient les séquences alignés
            except:
                return

            seqList = list() # Liste des séquences
            seqLen = 0 # Longueur des séquences
            positionList = list() # Liste des positions avec erreurs de nucléotides
            hNucList = list() # Liste des nucléotides à la position d'erreurs pour l'Homme
            cSNucList = list() # Liste des nucléotides à la position d'erreurs pour la chauve-souris
            pangNucList = list() # Liste des nucléotides à la position d'erreurs pour le pangolin

            # Deux variables de conservations des nucléotides
            conservPangNuc = 0
            conservBatNuc = 0

            errorList = list() # Liste d'erreur

            for seq in ensSeq:
                seqList.append(seq.seq)
                seqLen = len(seq.seq)
            
            result = "Position" + "\t" + "Homme" + "\t" + "Chauve-Souris" + "\t\t" + "Pangolin" + "\n\n"

            # Boucle d'écriture dans le fichier ; Mise en page avec les tabulations
            for a in range(seqLen): # l'opération se répète 1275 fois
                if seqList[0][a] != seqList[1][a]:
                    positionList.append(a)
                    hNucList.append(seqList[0][a])
                    cSNucList.append(seqList[1][a])
                    pangNucList.append(seqList[2][a])
                    if(a > 1000):
                        result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t" + seqList[1][a] + "\t\t" + seqList[2][a]) + "\n"
                    else:
                        result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t" + seqList[1][a] + "\t\t" + seqList[2][a]) + "\n"
                elif seqList[0][a] != seqList[2][a]:
                    positionList.append(a)
                    hNucList.append(seqList[0][a])
                    cSNucList.append(seqList[1][a])
                    pangNucList.append(seqList[2][a])
                    if(a > 1000):
                        result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t" + seqList[1][a] + "\t\t" + seqList[2][a]) + "\n"
                    else:
                        result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t" + seqList[1][a] + "\t\t" + seqList[2][a]) + "\n"
                elif seqList[1][a] != seqList[2][a]:
                    positionList.append(a)
                    hNucList.append(seqList[0][a])
                    cSNucList.append(seqList[1][a])
                    pangNucList.append(seqList[2][a])
                    if(a > 1000):
                        result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t" + seqList[1][a] + "\t\t" + seqList[2][a]) + "\n"
                    else:
                        result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t" + seqList[1][a] + "\t\t" + seqList[2][a]) + "\n"
                
                if seqList[1][a] == seqList[0][a]:
                    conservBatNuc = conservBatNuc + 1

                if seqList[2][a] == seqList[0][a]:
                    conservPangNuc = conservPangNuc + 1

            # Opérations mathématiques pour obtenir le % ; Arrondis à deux chiffres après la virgule
            conservBatNuc = conservBatNuc / seqLen
            conservBatNuc = conservBatNuc * 100
            conservBatNuc = round(conservBatNuc, 2)

            conservPangNuc = conservPangNuc / seqLen
            conservPangNuc = conservPangNuc * 100
            conservPangNuc = round(conservPangNuc, 2)

            global writeRule
            if writeRule == True:
                file = open(repPath + "/Protéine " + gene + "/" + "resultatComparaison_gene " + gene + ".txt", "w")
                file.write(result)
                file.close()

            # Ajout des positions et des erreurs pour obtenir une liste finale
            errorList.append(positionList)
            errorList.append(hNucList)
            errorList.append(cSNucList)
            errorList.append(pangNucList)
            errorList.append(conservBatNuc)
            errorList.append(conservPangNuc)
            errorList.append(gene)

            return errorList # Retour de la liste

    def Etape_I(gene, result_Etape_B):
            if path.exists("Fichiers externes/Protéines/Protéine " + gene + "/" + gene + ".gb") == True:
                return # On empêche la création du fichier s'il existe déja

            listID = list() # Création de la liste d'identifiant
            for x in range(len(result_Etape_B[8])): # On obtient les listes d'identifiants pour le gènes sélectionnés
                if(result_Etape_B[8][x] == gene.lower()):
                    listID.append(result_Etape_B[9][x])

            GetGenSeqGB(gene, listID) # On appelle la fonction GetGenSeqGB qui créé automatiquement le fichier genbank

class Align():
    def WriteAlign(gene):
        global writeRule
        if writeRule == False:
            return


        try:
            Alignement.Main(gene)
            MakeLogs("L'opération d'alignement manuel pour le gène " + gene + " à parfaitement réussie")
        except:
            MakeLogs("L'opération d'alignement pour le gène " + gene + " n'a pas pu aboutir")  