import os
import argparse
import subprocess
import pymol2 as pymol
parser = argparse.ArgumentParser()
# an argument for the pdb file
parser.add_argument("pdb_file", help="Path to the PDB file")
args = parser.parse_args()
# Get the arguments
pdb_file = args.pdb_file

with pymol.PyMOL() as pm:
    pm.cmd.load(f"{pdb_file}")
    s = "all"
    pm.cmd.set_color('color_ile',[0.996,0.062,0.062])
    pm.cmd.set_color('color_phe',[0.996,0.109,0.109])
    pm.cmd.set_color('color_val',[0.992,0.156,0.156])
    pm.cmd.set_color('color_leu',[0.992,0.207,0.207])
    pm.cmd.set_color('color_trp',[0.992,0.254,0.254])
    pm.cmd.set_color('color_met',[0.988,0.301,0.301])
    pm.cmd.set_color('color_ala',[0.988,0.348,0.348])
    pm.cmd.set_color('color_gly',[0.984,0.394,0.394])
    pm.cmd.set_color('color_cys',[0.984,0.445,0.445])
    pm.cmd.set_color('color_tyr',[0.984,0.492,0.492])
    pm.cmd.set_color('color_pro',[0.980,0.539,0.539])
    pm.cmd.set_color('color_thr',[0.980,0.586,0.586])
    pm.cmd.set_color('color_ser',[0.980,0.637,0.637])
    pm.cmd.set_color('color_his',[0.977,0.684,0.684])
    pm.cmd.set_color('color_glu',[0.977,0.730,0.730])
    pm.cmd.set_color('color_asn',[0.973,0.777,0.777])
    pm.cmd.set_color('color_gln',[0.973,0.824,0.824])
    pm.cmd.set_color('color_asp',[0.973,0.875,0.875])
    pm.cmd.set_color('color_lys',[0.899,0.922,0.922])
    pm.cmd.set_color('color_arg',[0.899,0.969,0.969])
    pm.cmd.color("color_ile","("+s+" and resn ile)")
    pm.cmd.color("color_phe","("+s+" and resn phe)")
    pm.cmd.color("color_val","("+s+" and resn val)")
    pm.cmd.color("color_leu","("+s+" and resn leu)")
    pm.cmd.color("color_trp","("+s+" and resn trp)")
    pm.cmd.color("color_met","("+s+" and resn met)")
    pm.cmd.color("color_ala","("+s+" and resn ala)")
    pm.cmd.color("color_gly","("+s+" and resn gly)")
    pm.cmd.color("color_cys","("+s+" and resn cys)")
    pm.cmd.color("color_tyr","("+s+" and resn tyr)")
    pm.cmd.color("color_pro","("+s+" and resn pro)")
    pm.cmd.color("color_thr","("+s+" and resn thr)")
    pm.cmd.color("color_ser","("+s+" and resn ser)")
    pm.cmd.color("color_his","("+s+" and resn his)")
    pm.cmd.color("color_glu","("+s+" and resn glu)")
    pm.cmd.color("color_asn","("+s+" and resn asn)")
    pm.cmd.color("color_gln","("+s+" and resn gln)")
    pm.cmd.color("color_asp","("+s+" and resn asp)")
    pm.cmd.color("color_lys","("+s+" and resn lys)")
    pm.cmd.color("color_arg","("+s+" and resn arg)")
    pm.cmd.do("z vis")
    pm.cmd.do("set ambient, 0.45")
    pm.cmd.do("set field_of_view, 40")
    pm.cmd.do("orient")
    pm.cmd.png("local_analysis/" + pdb_file.split("/")[-1].split(".")[0] + "_colorh.png")

#pm.color_h()



#pm.stop()
