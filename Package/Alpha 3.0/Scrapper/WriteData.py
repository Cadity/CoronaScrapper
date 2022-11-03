# Fonction de lecture du fichier seq_covid.gb
# et d'écriture dans le fichier info_seq_covid.txt

# Import des module
from Bio import SeqIO 
from Bio.SeqUtils import GC # Module de calcul du taux de GC

def MainFunction():
    ensSeq = SeqIO.parse("seq_covid.gb", "genbank") #Parse des trois séquences

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
                geneList.append(i.qualifiers["gene"][0]) # Obtention du nom de gène et inclusion dans la liste de gène
                locationStartList.append(i.location.start) # Obtention de la position de départ du gène actuel et inclusion dans la liste de position de départ
                locationEndList.append(i.location.end) # Obtention de la position de fin du gène actuel et inclusion dans la liste de position de départ
        listGeneNumber.append(number) # Sortie de boucle et ajout de la variable number à la liste de nombre de gènes pour chaque virus

    # Définition de finalText, string qui sera écrite dans info_seq_covid.txt
    finalText = "Informations complémentaires sur les Coronavirus :\n(Source : NCBI)\n\n"

    count = 0 
    for a in range(seqCount): # Boucle for dans un range du nombre de virus trouvé (pas de dépassement d'index) a prenant la définition d'un entier
        finalText = finalText + listName[a] + "\n" # Ecriture du nom
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
            finalText = finalText + "\t\t" + geneList[x] + " -> " + str(locationStartList[x]) + "..." + str(locationEndList[x]) + "\n" # Ecriture sur la même ligne du nom du gène et des positions
        count = count + listGeneNumber[a] # Addition de count et du nombre de gène -> Nouveau point de départ
        finalText = finalText + "\t}\n\n" # Rédation de la fin de la section virus

    # Ecriture dans le fichier info_seq_covid.txt en mode "effacement" ("w")    
    file = open("info_seq_covid.txt", "w")
    file.write(finalText)
    file.close()

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
    return fullDataList

MainFunction()