import sys
import glob
import os

def read_scores(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("REMARK VINA RESULT:"):
                return float(line.split(':')[1])

def doit(n):
    file_names = glob.glob('*/*.pdbqt')
    everything = []
    failures = []
    print('Found', len(file_names), 'pdbqt files')
    for file_name in file_names:
        result_file = os.path.join(os.path.dirname(file_name), 'results.txt')
        try:
            score = read_scores(result_file)
            everything.append([score, file_name])
        except Exception as e:
            failures.append(file_name)
    everything.sort(reverse=True)  # Sort in descending order based on score
    part = everything[:n]
    for p in part:
        print(os.path.basename(p[1]), '-', p[0])
    print()
    if len(failures) > 0:
        print('WARNING:', len(failures), 'pdbqt files could not be processed')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 script_name.py <number_of_files>")
        sys.exit(1)
    doit(int(sys.argv[1]))

