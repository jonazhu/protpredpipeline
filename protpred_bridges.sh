#!/bin/bash

echo "Starting ProtPred Pipeline."
echo "Activating Environment..."

eval "$(conda shell.bash hook)"
conda activate esmfold

echo "Environment activated."
echo "Processing proteins..."
python step1_final.py $1 $2 $3
echo "Protein sequences obtained."
echo "Running ESMFold..."
mkdir $4
cp $PROJECT/$2 $PROJECT/$4
cd $4

#to add: step that copies the list file here
#this is specifically for one-change things
bash ../step2_esm.sh ../homomer.fasta
cd ..
echo "ESMFold finished running. Use resulting directory of PDB files on a local machine with PyMol."
