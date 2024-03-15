#This script is generated to get the list of all compounds autodock vina result folders
#keep this file in same directory and open terminal
#run pyhton this_script_name.py ; you can add > top10List.txt at end of command to get text

import os

def get_score(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('   1'):
                return float(line.split()[1])
    return None

def list_scores():
    folders = [folder for folder in os.listdir() if os.path.isdir(folder)]
    scores = []
    for folder in folders:
        result_file = os.path.join(folder, 'results.txt')
        if os.path.exists(result_file):
            score = get_score(result_file)
            if score is not None:  # Check if score is valid
                scores.append((folder, score))
    # Sort scores in descending order based on score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

if __name__ == '__main__':
    scores = list_scores()
    for folder, score in scores:
        print(f"{folder} {score}")

