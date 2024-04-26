#!/bin/bash

#shell to install ESMFold based on the guidelines posted by the TA.
#if this is wrong, tough luck.
echo "Getting ESMFold files..."
git clone https://github.com/facebookresearch/esm.git
echo "Files retrieved successfully."
echo "Creating environment..."
conda env create -f esm/environment.yml
echo "Environment creation successful."
