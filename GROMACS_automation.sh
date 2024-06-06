#!/bin/bash

# Function to display folders and get user selection
select_folders() {
    echo "Available folders:"
    options=($(ls -d */))
    for i in "${!options[@]}"; do
        echo "$((i+1))) ${options[$i]}"
    done
    echo "$(( ${#options[@]} + 1 ))) Done"

    selected_folders=()
    while true; do
        read -p "Select folders (enter numbers separated by spaces, press 'd' when done): " -a selections
        for selection in "${selections[@]}"; do
            if [[ "$selection" == "d" ]]; then
                return
            elif [[ "$selection" -ge 1 && "$selection" -le "${#options[@]}" ]]; then
                folder="${options[$((selection-1))]}"
                if [[ ! " ${selected_folders[@]} " =~ " ${folder} " ]]; then
                    selected_folders+=("$folder")
                    echo "Selected: $folder"
                else
                    echo "Already selected: $folder"
                fi
            else
                echo "Invalid option: $selection"
            fi
        done
    done
}

# Function to run the command in each selected folder
run_command_in_folders() {
    for folder in "${selected_folders[@]}"; do
        echo "Processing folder: $folder"
        cd "$folder" || continue
        echo -e "1|13\nq" | gmx make_ndx -f em.gro -o index.ndx && gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr && gmx mdrun -deffnm nvt -nb gpu -v && gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r nvt.gro -p topol.top -n index.ndx -o npt.tpr -maxwarn 1 && gmx mdrun -deffnm npt -nb gpu -v && gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md_0_10.tpr && gmx mdrun -deffnm md_0_10 -nb gpu -v && gmx trjconv -s md_0_10.tpr -f md_0_10.xtc -o md_noPBC.xtc -pbc cluster -center -n -ur compact && gmx trjconv -s md_0_10.tpr -f md_noPBC.xtc -o md_noPBC1.xtc -pbc mol -center -n -ur compact && echo -e "1\n" | gmx trjconv -s md_0_10.tpr -f md_noPBC1.xtc -o start_protein.pdb -dump 0 ; echo -e "1\n" | gmx trjconv -s md_0_10.tpr -f md_noPBC1.xtc -o end_protein.pdb -dump 11000000 && echo -e "13\n" | gmx trjconv -s md_0_10.tpr -f md_noPBC1.xtc -o start_LIG.pdb -dump 0 ;  echo -e "13\n" | gmx trjconv -s md_0_10.tpr -f md_noPBC1.xtc -o end_LIG.pdb -dump 11000000 ;  echo -e "20\n" | gmx trjconv -s md_0_10.tpr -f md_noPBC1.xtc -o start_complex_Prot_LIG.pdb -dump 0 -n index.ndx ; echo -e "20\n" | gmx trjconv -s md_0_10.tpr -f md_noPBC1.xtc -o end_complex_Prot_LIG.pdb -dump 11000000 -n index.ndx && echo -e "1\n1" | gmx rms -s md_0_10.tpr -f md_noPBC1.xtc -o rmsd_protein.xvg -tu ns -n index.ndx && echo -e "1\n13" | gmx rms -s md_0_10.tpr -f md_noPBC1.xtc -o rmsd_LIG.xvg -tu ns -n index.ndx && echo -e "1\n" | gmx rmsf -s md_0_10.tpr -f md_noPBC1.xtc -o rmsf_residue.xvg -res -n index.ndx &&  echo -e "1\n" | gmx gyrate -s md_0_10.tpr -f md_noPBC1.xtc -o rg.xvg -n index.ndx && echo -e "1\n13" | gmx hbond -s md_0_10.tpr -f md_noPBC1.xtc -num hbond.xvg -n index.ndx && echo -e "9 10 0\n" | gmx energy -f md_0_10.edr -o interaction_energy.xvg
        cd ..
    done
}

# Main script execution
select_folders
run_command_in_folders
