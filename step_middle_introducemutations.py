# %%
from Bio.Seq import Seq
import pyfaidx
#from Bio import Entrez
import requests
from Bio import SeqIO
from io import StringIO
from Bio.SeqRecord import SeqRecord
import sys

# %%
#read FASTA file
def ReadFasta(file):
    """
    ReadFasta() takes in the name of a FASTA file and returns a list of all the
    sequences in the file, and a list of all the records that match the sequences.
    """
    genes = pyfaidx.Fasta(file)
    records = list(genes.keys())
    seqs = []
    for i in range(len(records)):
        seq1 = genes[records[i]][:].seq
        seqs.append(seq1)
    
    return records, seqs

# %%
def IntroduceMutation(sequence, pos, mut):
    """ 
    IntroduceMutation() takes in a sequence of amino acids, a position to change,
    and the new amino acid to change to. Hypothetically this can work with DNA too.
    Critically, it is a string, not a Sequence object.
    """
    newseq = sequence[0:pos+1] + mut + sequence[pos+2:]
    return newseq

# %%
def WriteFasta(s, r, filename = "homomer.fasta"):
    """
    WriteFasta() takes in a list of sequence strings, a list of record ids, and
    an output filename (optional), writing a fasta file containing each one.
    """
    items = []
    for i in range(len(s)):
        record = SeqRecord(Seq(s[i]), id = r[i] + "_mutation_" + str(i))
        if i == 0:
            record = SeqRecord(Seq(s[i]), id = r[i] + "_wildtype")
        items.append(record)
    SeqIO.write(items, filename, "fasta")

# %%
def ReadMutations(filename):
    """ 
    If you want to introduce multiple mutations into the same protein, provide
    a text file with the position and mutation match on each line, with those
    parts separated by a space. ReadMutations() will return the list
    of positions and the matching mutations.
    """
    positions = []
    mutations = []
    with open(filename, "r") as fr:
        for line in fr:
            parts = line.split()
            positions.append(int(parts[0]))
            mutations.append(parts[1])
    
    return positions, mutations

# %%
def ImplementMutations(prot, record, pos, mut):
    """
    Basically IntroduceMutation() but for many mutations given in pos and mut.
    Note that it returns a list of records the same length, this is for
    ease of writing later.
    """
    prots = []
    prots.append(prot)
    records = []
    records.append(record)
    for i in range(len(pos)):
        current_seq = IntroduceMutation(prot, pos[i], mut[i])
        prots.append(current_seq)
        records.append(record)
    
    return prots, records

# %%
if __name__ == "__main__":
    test_record, test_seq = ReadFasta(sys.argv[1])
    p, m = ReadMutations(sys.argv[2])
    s, r = ImplementMutations(test_seq[0], test_record[0], p, m)
    WriteFasta(s, r)


