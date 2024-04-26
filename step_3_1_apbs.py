import os
import shutil
from pymol import cmd
from pmg_tk.startup.apbs_gui.electrostatics import map_new_apbs
from pmg_tk.startup.apbs_gui.creating import pdb2pqr_cli

filename = sys.argv[1]
pdb_res = sys.argv[2]
output = sys.argv[3]
print(filename, pdb_res)
def run_apbs(file_name, pdb_res):
    

    # If a folder doesnt exist make a new folder called apbs
    if not os.path.exists('apbs'):
        os.makedirs('apbs')
    
    fname = file_name.split('.')[0]
    cmd.load(file_name, fname)
    
    pdb2pqr_cli('prep', fname, options = ['--ff', 'AMBER'])
    map_new_apbs('apbs_map', 'prep')
    
    cmd.ramp_new("apbs_ramp", "apbs_map", [-2.5, 0, 2.5])
    cmd.set("surface_ramp_above_mode", 1, "prep")
    cmd.set("surface_color", "apbs_ramp", "prep")
    cmd.hide("everything", "all")
    cmd.select(f'all within 12 of resi {pdb_res}')
    cmd.show("surface", "sele")
    cmd.hide("everything", f'{fname}')
    cmd.zoom(f'resi {pdb_res}', 15)
    cmd.set("ambient", "0.25")
    cmd.set("field_of_view", "20")
    cmd.delete("sele")
    cmd.png(f'{output}', ray=1)
     
    # move fname_apbs.png to apbs folder
    shutil.move(f'{output}', f'APBS/{output}')

cmd.extend("run_apbs", run_apbs)
run_apbs(filename, pdb_res)
cmd.do("quit")
