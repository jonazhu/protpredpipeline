import torch
import esm
import pyfaidx
import step_middle_introducemutations as im
import sys

#the following needs to be added in shell for proper storage of data
#ive done it on my sector of Bridges but this is for future reference.
#os.environ("TORCH_HOME") = "$PROJECT/torch_cache"
#or you can use the shell command 
#export TORCH_HOME=/ocean/projects/bio230007p/{ur_user_id}/torch_cache

model = esm.pretrained.esmfold_v1()
model = model.eval().cuda()

#get the sequences
records, seqs = im.ReadFasta(sys.argv[1]) #fasta name to read in

#test sequence
#sequence = "MKTVRQERLKSIVRILERSKEPVSGAGLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"

with torch.no_grad():
    outputs = []
    for s in seqs:
        outputs.append(model.infer_pdb(s))

for i in range(len(outputs)):
    currentname = "result" + str(i) + ".pdb"
    with open(currentname, "w") as f:
        f.write(outputs[i])