#import packages, including various from previous scripts
import step1_getfastas as gf
import step_middle_introducemutations as im
import sys

if __name__ == "__main__":
    #change depending on option
    if sys.argv[1] == "ids":
        #option 1: list of IDs
        file = sys.argv[2]
        ids = gf.read_file(file)
        seqs = gf.get_prots(ids)
        gf.write_prots(seqs)
    elif sys.argv[1] == "onechange":
        #option 2: list changes, and each one is a separate change
        #so 3 changes listed will yield 3 altered proteins.
        #must also provide a fasta file as the third arg

        test_record, test_seq = im.ReadFasta(sys.argv[3])
        p, m = im.ReadMutations(sys.argv[2])
        s, r = im.ImplementMutations(test_seq[0], test_record[0], p, m)
        im.WriteFasta(s, r)
    elif sys.argv[1] == "multichange":
        #option 3: list changes, and all occur on the same prot
        #so 3 changes listed will yield only 1 altered protein.
        #must also provide a fasta file as the third arg
        test_record, test_seq = im.ReadFasta(sys.argv[3])
        p, m = im.ReadMutations(sys.argv[2])
        t1, t2 = im.ImplementMultiMut(test_seq[0], test_record[0], p, m)
        s = [t1]
        r = [t2]
        im.WriteFasta(s, r)
    else:
        print("Invalid option given for getting protein sequences")