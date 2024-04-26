#!/bin/bash

echo "Loading modules..."
conda install -c conda-forge einops=0.6.1
module load cuda/11.7.1
echo "Modules loaded successfully."

echo "Installing dependencies..."
pip install "fair-esm[esmfold]"
pip install 'dllogger @ git+https://github.com/NVIDIA/dllogger.git'
pip install 'openfold @ git+https://github.com/aqlaboratory/openfold.git@4b41059694619831a7db195b7e0988fc4ff3a307'
pip install git+https://github.com/facebookresearch/esm.git
echo "Dependencies installed."

mkdir torch_cache