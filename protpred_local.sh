#!/bin/bash
# This script takes in a directory of protein structures and performs analysis on the predicted structures.
# It assumes that a specific conda environment is already activated.

# Initialize variables to store the ligand file and the directory of protein structures.
docking_ligand=""
protein_structures=""

# Process command line options using getopts.
# -d for specifying the docking ligand.
# -f for specifying the directory of protein structures.
while getopts ":d:f:" opt; do
  case $opt in
    d)  docking_ligand=$OPTARG ;; # Assign the argument to docking_ligand when -d is used
    f)  protein_structures=$OPTARG ;; # Assign the directory to protein_structures when -f is used
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;; # Handle invalid options
    :)  echo "Option -$OPTARG requires an argument." >&2; exit 1 ;; # Handle missing option arguments
  esac
done

# Validate that the protein structures directory has been set.
if [[ -z "$protein_structures" ]]; then
    echo "Error: Protein structures directory must be specified with -f option."
    exit 1
fi

# Step 3 - Perform RMSD (Root Mean Square Deviation) analysis on predicted structures.
echo "Performing RMSD calculations"
mkdir local_analysis # Create a directory to store analysis results
python3 step_3_align.py "$protein_structures" # Run RMSD analysis script
mv distance_matrix.txt local_analysis # Move the distance matrix to analysis directory
mv pdb_files_order.txt local_analysis # Move pdb files order list to analysis directory

# Step 3.1 - Run APBS (Adaptive Poisson-Boltzmann Solver) on the predicted structures.
echo "PERFORMING APBS CALCULATIONS"
mkdir APBS # Directory for APBS output
files=$(ls "$protein_structures"/*.pdb) # List all .pdb files in the given directory
# Read mutations from a file and store them in an array
IFS=$'\n' read -d '' -r -a muts < <(awk '{print $1}' "$protein_structures/muts.txt" && printf '\0')
count=0
for mut in "${muts[@]}"; do
    echo "$mut" # Print mutation information
done

# Loop through each file to process APBS calculations
for file in $files; do
    if (( $count == 0 )); then
        echo "Processing wild type!" # Special handling for the first (wild type) file
        cp "$file" ./ # Copy the file to the current directory
        for mut in "${muts[@]}"; do
            filename="$(basename "$file")"
            pymol step_3_1_apbs.py -- $filename $mut "result0_${count}_${mut}.png"
        done
        rm $filename # Remove the copied file
    elif (($count>=1)); then
        echo "Processing mutant structure!"
        filename="$(basename "$file")"
        cp "$file" ./${filename}
        echo "pymol step_3_1_apbs.py -- ${filename} ${muts[count-1]} ${filename}.png"
        pymol step_3_1_apbs.py -- ${filename} ${muts[count-1]} ${filename}.png
        rm ${filename}
    fi
    let "count++"
done

mv APBS local_analysis # Move APBS directory to local_analysis

# Step 4 - Perform light dock if docking ligand was provided.
if [[ -n $docking_ligand ]]; then
    echo "Performing lightdock calculations"
    for file in $files; do
        echo $file
        python3 step_4_docking.py $file $docking_ligand # Dock each protein with the ligand
    done
fi

# Step 5 - Create a heatmap from RMSD data.
echo "Creating heatmap"
cp local_analysis/distance_matrix.txt ./ # Copy the distance matrix file for heatmap generation
python3 step_5_heatmap.py distance_matrix.txt # Generate heatmap
mv RMSD_heatmap.png local_analysis # Move the heatmap image to analysis directory
rm distance_matrix.txt # Clean up the distance matrix file

# Step 5 - Color structures based on hydrophobicity.
echo "Performing coloring via hydrophobicity"
for file in "$protein_structures"/*.pdb; do
    python3 step_6_props.py $file # Apply hydrophobicity coloring to each file
done

echo "Analysis complete!"
echo "Please check the local_analysis folder for the results."

