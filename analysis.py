import re

# Function to parse the result.txt file
def parse_result_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extracting ligand information
    ligand_matches = re.findall(r'Refining ligand \./test_out/(\d+) results(.*?)(?=(?:Refining ligand \./test_out/|\Z))', content, re.DOTALL)

    # Organize the data into a list of dictionaries
    ligand_data = [{'ligand_id': match[0], 'result_data': match[1].strip()} for match in ligand_matches]

    return ligand_data

# Function to get the top N ligands based on docking score
def get_top_ligands(ligand_data, top_n=10):
    # Extracting docking score from result_data
    for ligand in ligand_data:
        scores = re.findall(r'\d+\s+(-?\d+\.\d+)\s+\d+\.\d+\s+\d+\.\d+', ligand['result_data'])
        if scores:
            ligand['docking_score'] = float(scores[0])

    # Remove ligands without docking score
    ligand_data = [ligand for ligand in ligand_data if 'docking_score' in ligand]

    # Sort ligands based on docking score
    sorted_ligands = sorted(ligand_data, key=lambda x: x['docking_score'], reverse=True)

    return sorted_ligands[:top_n]

# Specify the path to the result.txt file
result_file_path = './result.txt'

# Parse the result file
ligand_data = parse_result_file(result_file_path)

# Get the top 10 ligands
top_ligands = get_top_ligands(ligand_data, top_n=10)

# Display the results
print("Top 10 Ligands:")
for i, ligand in enumerate(top_ligands, start=1):
    print(f"{i}. Ligand {ligand['ligand_id']} - Docking Score: {ligand['docking_score']}")
