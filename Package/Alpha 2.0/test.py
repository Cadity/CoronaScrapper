
from Bio import Entrez
from Bio import SeqIO

Entrez.email = "antoinetavoillot@gmail.com"
maReq = Entrez.esearch(db="nucleotide", term="SARS-COV 2[orgn] AND srcdb_refseq [SPIKE]", rettype="gb")
res = Entrez.read(maReq)
newReq = Entrez.efetch(db = "nucleotide", id=res["IdList"][0], rettype="gb")
maSeq = SeqIO.read(newReq, "gb")
print(maSeq)