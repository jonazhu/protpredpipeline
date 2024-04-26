CONDA_SUBDIR=osx-64 conda create -n protpredlocal #-f local_env.yml
conda init --all
eval "$(conda shell.bash hook)"
conda activate protpredlocal
conda install pip
CONDA_SUBDIR=osx-64 conda env update -n protpredlocal --file local_env.yml
pip install --use-pep517 lightdock
pip install --use-pep517 prody
pip install pyparsing==3.1.1
chmod +x protpred_local.sh
