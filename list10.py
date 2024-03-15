#This script is generated to get the list of top 10 compounds autodock vina result folders
#keep this file in same directory and open terminal
#run pyhton this_script_name.py ; you can add > top10List.txt at end of command to get text

import os

def get_score(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('   1'):
                return float(line.split()[1])

def get_top_scores():
    folders = [folder for folder in os.listdir() if os.path.isdir(folder)]
    top_scores = []
    for folder in folders:
        result_file = os.path.join(folder, 'results.txt')
        if os.path.exists(result_file):
            score = get_score(result_file)
            top_scores.append((folder, score))
    top_scores.sort(key=lambda x: x[1], reverse=False)
    return top_scores

if __name__ == '__main__':
    top_scores = get_top_scores()
    for folder, score in top_scores:
        print(f"{folder} {score}")

