import os

def extract_first_model_from_pdbqt(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdbqt"):
            with open(os.path.join(folder_path, filename), 'r') as pdbqt_file:
                lines = pdbqt_file.readlines()
                model_number = 0
                output_lines = []
                for line in lines:
                    if line.startswith("MODEL"):
                        model_number += 1
                    elif line.startswith("ENDMDL"):
                        if model_number == 1:
                            break
                    elif model_number == 1:
                        output_lines.append(line)

            # Write extracted first model to a new file
            output_filename = f"m1_{folder_name}.pdbqt"
            with open(output_filename, 'w') as output_file:
                output_file.write("".join(output_lines))
            break  # Exit loop after processing the first .pdbqt file

# Use the current directory as the directory path
directory_path = "."

# Iterate through each folder in the directory
for folder_name in os.listdir(directory_path):
    folder_path = os.path.join(directory_path, folder_name)
    if os.path.isdir(folder_path):
        extract_first_model_from_pdbqt(folder_path)

