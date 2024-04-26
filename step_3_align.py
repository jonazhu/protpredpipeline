import pymol2
import argparse
import os



# Takes in a directory file name
args = argparse.ArgumentParser()
args.add_argument("directory", help="Directory containing pdb files.")
args = args.parse_args()

directory = args.directory
pdb_files = []
for file in os.listdir(directory):
    if file.endswith(".pdb"):
        pdb_files.append(file)

# Change into the given directory.
os.chdir(directory)

# Takes in a list of pdb files and aligns them to each other and returns a distance matrix of the RMSD values.

def align(pdb_files) -> list:
    """
    Input: List of pdb files in given directory.
    Output: Distance matrix of RMSD values.
    """
    dist_mat = [[0.0 for _ in range(len(pdb_files))] for _ in range(len(pdb_files))]
    for i, file in enumerate(pdb_files):
        for j, file2 in enumerate(pdb_files):
            if i != j:
                with pymol2.PyMOL() as pm:
                    file1_name = file.split(".")[0]
                    file2_name = file2.split(".")[0]
                    pm.cmd.load(file, file1_name)
                    pm.cmd.load(file2, file2_name)
                    out = pm.cmd.super(file1_name, file2_name)
                    dist_mat[i][j] = out[0]
            else:
                dist_mat[i][j] = 0.0
    return dist_mat


def write_dist_mat(dist_mat, pdb_files) -> None:
    """
    Input: Distance matrix of RMSD values, list of pdb files.
    Output: Writes distance matrix to a file.
    """
    with open("distance_matrix.txt", "w") as f:
        for idx in range(len(dist_mat)):
            for idy in range(len(dist_mat)):
                f.write(str(dist_mat[idx][idy]) + " ")
            f.write("\n")
        f.close()

    with open("pdb_files_order.txt", "w") as f:
        for file in pdb_files:
            f.write(file + "\n")
        f.close()

# Change back to the higher directory.
alignments = align(pdb_files)
os.chdir("..")

write_dist_mat(alignments, pdb_files)

    
