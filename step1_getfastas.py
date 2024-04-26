# %%
import sys
import requests
from io import StringIO

# %%
#portion to get it into alphafold.
#alphafold accepts fasta files so we need to get all the seqs we want and put them into a fasta file

#for this we will use entrez
def get_prots(ids):
    seqs = []
    for i in ids:
        current_url = "https://rest.uniprot.org/uniprotkb/" + i + ".fasta"

        response = requests.post(current_url)
        cData=''.join(response.text)

        #Seq=StringIO(cData)
        #pSeq=list(SeqIO.parse(Seq,'fasta'))
        seqs.append(cData)

    return seqs

# %%
#the file ORFs.fasta will have the orfs found, while the file prots.txt and mw.txt will have the protein sequences and the weights.
def write_prots(seqs):
    with open("homomer.fasta", "w") as fw:
        for s in seqs:
            fw.write(s)
            fw.write("\n")

#read the ids from a filename
def read_file(filename):
    with open(filename, "r") as fr:
        ids = []
        for line in fr:
            n = len(line)
            current_id = line
            if line[n-1] == "\n":
                current_id = line[:n-1]
            ids.append(current_id)

    return ids

# %%
if __name__ == "__main__":
    file = sys.argv[1]
    ids = read_file(file)
    seqs = get_prots(ids)
    write_prots(seqs)



