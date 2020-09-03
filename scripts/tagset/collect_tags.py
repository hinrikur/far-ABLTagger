import sys 
import re
from collections import defaultdict

"""
Collects tags in tagged corpus file (token\ttag format)

Usage:
    python3 collect_tags.py path/to/file.txt (path/to/output/folder if wanted) 

"""

IN_FILE = OUT_FOLDER = None

if len(sys.argv) == 1:
    print('Must write file argument!')
    exit()
elif len(sys.argv) == 2:
    IN_FILE = sys.argv[1]
elif len(sys.argv) == 3:
    IN_FILE = sys.argv[1]
    OUT_FOLDER = sys.argv[2]

tags = defaultdict(int)

with open(IN_FILE, 'r') as f:
    for line in f.readlines():
        # print(line)
        if re.search(r'(^\%\%|^$)', line): continue
        # print(line)
        tag = line.split('\t')[1].strip('\n')
        tags[tag] += 1
        
# for k,v in sorted(tags.items()):
#     print(k,v)
# input()

with open(OUT_FOLDER+'tags_alph.txt', 'w') if OUT_FOLDER else sys.stdout as f:
    for k,v in sorted(tags.items()):
        f.write(str(k)+'\t'+str(v)+'\n')
