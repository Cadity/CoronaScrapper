# Fonction de lecture du fichier seq_covid.gb
# et d'écriture dans le fichier info_seq_covid.txt

# Import des module
from Bio import SeqIO 
from Bio.SeqUtils import GC # Module de calcul du taux de GC
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Align.Applications import MafftCommandline

def MainFunction(gene, request): # Fonction principale -> Nom du gène en entrée ; Request : booléen pour éviter de renvoyer des requête à chaque fois
    finalList = list() # Déclaration de la liste qui permettra de retourner les éléments sur la fenêtre principale
    if request == True: # En cas de demande de requête
        mainList = Etape_B() # On fait la requête et on ajoute la liste retournée à la liste principale
        finalList.append(mainList)
    Etape_C(gene) # Etape C
    Etape_D(gene) # Etape D
    errorList = Etape_E(gene) # On récupère la liste des différences entre les séquences
    finalList.append(errorList)
    return finalList # On retourne la liste finale

def Etape_B():
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

    # On définit une boucle while pour vérifier qu'un CDS n'a pas deux fois le même identifiants
    countOccur = 0
    while countOccur < len(newGeneList) - 1:
        if newGeneList[countOccur] == newGeneList[countOccur + 1]:
            # Si c'est le cas, on rattache les deux identifiants ensemble afin d'obtenir une liste d'identifiant de gènes de la même taille que la liste de gène
            idProteinList[countOccur] = idProteinList[countOccur] + " / " + idProteinList[countOccur + 1]
            idProteinList.pop(countOccur + 1)
        countOccur = countOccur + 1

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
    fullDataList.append(geneList)
    fullDataList.append(idProteinList)
    fullDataList.append(locationStartList)
    fullDataList.append(locationEndList)
    return fullDataList

def GetGenList():
    test = Etape_B()[8]
    tempGenList = list()
    finalGenList = list()

    for a in test:
        if(test.count(a) == 3):
            if a not in tempGenList:
                gen = a.upper()
                tempGenList.append(a)
                finalGenList.append("Protéine " + gen)

    return finalGenList

def Etape_C(gene):
    ensSeq = SeqIO.parse("seq_covid.gb", "genbank") #Parse des trois séquences

    listSeqRecord = list() # Définition de la liste des SeqRecord
    currentVirus = "" # Définition d'une variable currentVirus pour connaître le virus étudié à un instant T
    for seq in ensSeq: # Boucle for, seq prends la valeur de l'occurence de ensSeq à chaque itération
        currentVirus = seq.description # On attribue seq.description à currentVirus à chaque itération
        for i in seq.features: # Boucle for, on recherche dans les features de Seq
            if i.type == "CDS": # On affine la recherche ; uniquement le feature de type CDS
                if i.qualifiers["gene"][0] == gene: # On affine la recherche ; uniquement si le gène actuel est S, pour "Spike"
                    listSeqRecord.append(SeqRecord(Seq(i.qualifiers["translation"][0]), id=i.qualifiers["protein_id"][0], name=i.qualifiers["gene"][0], description=currentVirus + ", " + i.qualifiers["product"][0])) # On rempli la liste de SeqRecord

    name = gene

    if gene == "S":
        name = "spike"
    SeqIO.write(listSeqRecord, name + ".fasta", "fasta") # On écris les SeqRecord dans le fichier spike.fasta au format fasta

def Etape_E(gene):

    alnFileName = ""
    if gene == "S":
        alnFileName = "spike"
    else:
        alnFileName = gene

    ensSeq = SeqIO.parse("aln-" + alnFileName + ".fasta", "fasta") # On obtient les séquences alignés

    seqList = list() #
    seqLen = 0
    positionList = list() # Liste des positions avec erreurs de nucléotides
    hNucList = list() # Liste des nucléotides à la position d'erreurs pour l'Homme
    cSNucList = list() # Liste des nucléotides à la position d'erreurs pour la chauve-souris
    pangNucList = list() # Liste des nucléotides à la position d'erreurs pour le pangolin

    conservPangNuc = 0
    conservBatNuc = 0

    errorList = list()

    for seq in ensSeq:
        seqList.append(seq.seq)
        seqLen = len(seq.seq)
    
    result = "Position" + "\t" + "Homme" + "\t" + "Chauve-Souris" + "\t" + "Pangolin" + "\n"

    for a in range(seqLen): # l'opération se répète 1275 fois
        if seqList[0][a] != seqList[1][a]:
            positionList.append(a)
            hNucList.append(seqList[0][a])
            cSNucList.append(seqList[1][a])
            pangNucList.append(seqList[2][a])
            if(a > 1000):
                result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t\t" + seqList[1][a] + "\t\t\t\t" + seqList[2][a]) + "\n"
            else:
                result = result + (str(a) + "\t\t\t" + seqList[0][a] + "\t\t\t" + seqList[1][a] + "\t\t\t\t" + seqList[2][a]) + "\n"
        elif seqList[0][a] != seqList[2][a]:
            positionList.append(a)
            hNucList.append(seqList[0][a])
            cSNucList.append(seqList[1][a])
            pangNucList.append(seqList[2][a])
            if(a > 1000):
                result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t\t" + seqList[1][a] + "\t\t\t\t" + seqList[2][a]) + "\n"
            else:
                result = result + (str(a) + "\t\t\t" + seqList[0][a] + "\t\t\t" + seqList[1][a] + "\t\t\t\t" + seqList[2][a]) + "\n"
        elif seqList[1][a] != seqList[2][a]:
            positionList.append(a)
            hNucList.append(seqList[0][a])
            cSNucList.append(seqList[1][a])
            pangNucList.append(seqList[2][a])
            if(a > 1000):
                result = result + (str(a) + "\t\t" + seqList[0][a] + "\t\t\t" + seqList[1][a] + "\t\t\t\t" + seqList[2][a]) + "\n"
            else:
                result = result + (str(a) + "\t\t\t" + seqList[0][a] + "\t\t\t" + seqList[1][a] + "\t\t\t\t" + seqList[2][a]) + "\n"
        
        if seqList[1][a] == seqList[0][a]:
            conservBatNuc = conservBatNuc + 1

        if seqList[2][a] == seqList[0][a]:
            conservPangNuc = conservPangNuc + 1

    conservBatNuc = conservBatNuc / seqLen
    conservBatNuc = conservBatNuc * 100
    conservBatNuc = round(conservBatNuc, 2)

    conservPangNuc = conservPangNuc / seqLen
    conservPangNuc = conservPangNuc * 100
    conservPangNuc = round(conservPangNuc, 2)

    file = open("resultatComparaison_gene" + gene + ".txt", "w")
    file.write(result)
    file.close()

    errorList.append(positionList)
    errorList.append(hNucList)
    errorList.append(cSNucList)
    errorList.append(pangNucList)
    errorList.append(conservBatNuc)
    errorList.append(conservPangNuc)

    return errorList

def Etape_D(gene):

    fileName = ""

    if gene == "S":
        fileName = "spike"
    else:
        fileName = gene

    from Bio.Align.Applications import MafftCommandline
    commande = MafftCommandline(input= fileName + ".fasta")
    myStdout, myStderr = commande()
    with open("aln-" + fileName + ".fasta", 'w') as w:
        w.write(myStdout)

def WriteFile(gene):
    Etape_C(gene)
    Etape_D(gene)
