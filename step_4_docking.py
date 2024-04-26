import os
import argparse
import subprocess
import pymol2
import prody as pd

# 
# Create a directory called lightdock if the folder doesn't exist
if not os.path.exists("lightdock"):
    os.mkdir("lightdock")


# Read in two arguments filename of receptor and filename of ligand
parser = argparse.ArgumentParser()
parser.add_argument("receptor", help="filename of receptor")
parser.add_argument("ligand", help="filename of ligand")

args = parser.parse_args()

print("argparser")
receptor = args.receptor
ligand = args.ligand

rec_name = receptor.split(".")[0]

print("writing chains")
# Change the chain of the ligand to B
lig = pd.parsePDB(ligand)
lig.setChids("B")
pd.writePDB(ligand, lig)

# Copy the receptor and ligand files into lightdock
os.system("cp " + receptor + " lightdock")
os.system("cp " + ligand + " lightdock")



receptor = receptor.split("/")[-1]

# Run the docking
os.chdir("lightdock")

print(receptor, ligand)
subprocess.run(["lightdock3_setup.py", receptor, ligand, "-s 50", "-g 10"])


# Run the docking
subprocess.run(["lightdock3.py", "setup.json","100", "-l 0"])


# Iterate through each swarm


# Generate conformations
subprocess.run(["lgd_generate_conformations.py", receptor, ligand, "swarm_0/gso_100.out", "10"])

# Cluster conformations
subprocess.run(["lgd_cluster_bsas.py", "swarm_0/gso_100.out"])


# Get the top/best scoring docking pose.
with open("swarm_0/cluster.repr", "r") as f:
    lines = f.readlines()
    best_pose = lines[0].split(":")[-1]
    best_pose.strip('\n')
    f.close()


# Now we want to run pymol to visualize the best pose.
with pymol2.PyMOL() as pm:
    rec_name = receptor.split(".")[0]
    lig_name = ligand.split(".")[0]
    pose_name = best_pose.split(".")[0]
    print(best_pose)
    pm.cmd.load(f"swarm_0/{pose_name}" + ".pdb")
    pm.cmd.load(receptor)
    pm.cmd.load(ligand)
    pm.cmd.super(rec_name, pose_name)
    pm.cmd.super(lig_name, pose_name)
    pm.cmd.hide("everything")
    pm.cmd.show("surface", rec_name)
    pm.cmd.show("surface", lig_name)
    pm.cmd.do("util.cbc")
    pm.cmd.do("z vis")
    pm.cmd.do("set ambient, 0.45")
    pm.cmd.do("set field_of_view, 40")
    pm.cmd.do("orient")
    pm.cmd.png(f"best_pose_{rec_name}.png", dpi=300, ray=1)
    pm.cmd.save("pose_sess.pse")

os.system(f"mv best_pose_{rec_name}.png ../local_analysis")
os.chdir("..")
# Move lightdock to best directory.
os.system("rm -rf lightdock")
