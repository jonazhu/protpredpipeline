#!/bin/bash

#previously I had the following:
#module load AI
#conda activate esmfold
#these need to be activated BEFORE step 1!!!!

export TORCH_HOME=$PROJECT/torch_cache
python ../test_esm.py $1 