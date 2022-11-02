from asyncore import write
from Bio import SeqIO, SeqRecord, SeqFeature
from Bio.SeqUtils import GC
from Bio.Seq import Seq

def MainFunction():
    ensSeq = SeqIO.parse("seq_covid.gb", "genbank")

    seqCount = 0
    listName = list()
    listHost = list()
    listTaxonomieId = list()
    listAccessionsId = list()
    listCreationDate = list()
    listGeneNumber = list()
    listGCRate = list()

    for seq in ensSeq:
        mesSeqF = seq.features
        listName.append(seq.annotations["organism"])
        listAccessionsId.append(seq.id)
        number = 0
        seqCount = seqCount + 1
        listGCRate.append(round(GC(seq.seq), 2))
        for i in mesSeqF:
            if i.type == "source":
                listHost.append(i.qualifiers["host"][0])
                listTaxonomieId.append(i.qualifiers["db_xref"][0].split("taxon:")[1])
                listCreationDate.append(i.qualifiers["collection_date"][0])
            if i.type == "gene":
                number = number + 1
        listGeneNumber.append(number)

    finalText = "Informations complémentaires sur les Coronavirus :\n(Source : NCBI)\n\n"

    for a in range(seqCount):
        finalText = finalText + listName[a] + "\n"
        finalText = finalText + "\tOrganisme : " + listHost[a] + "\n"
        finalText = finalText + "\tIdentifiant taxonomique : " + listTaxonomieId[a] + "\n"
        finalText = finalText + "\tNuméro d'accession de la donnée GenBank : " + str(listAccessionsId[a]) + "\n"
        finalText = finalText + "\tDate de création de la donnée GenBank : " + listCreationDate[a] + "\n"
        finalText = finalText + "\tNombre de gène : " + str(listGeneNumber[a]) + "\n"
        finalText = finalText + "\tTaux de GC : " + str(listGCRate[a]) + "\n"
        finalText = finalText + "\n"

    file = open("info_seq_covid.txt", "w")
    file.write(finalText)
    file.close()

    #Retour d'une liste de liste avec l'ensemble des données
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