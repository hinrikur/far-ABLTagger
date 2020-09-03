import sys
import re
import os
from collections import defaultdict

FILE = sys.argv[1] # path to file as first argument
SENT_NUM = int(sys.argv[2]) # number of output sentences 
# PARENT_FOLDER = os.path.dirname(FILE) # parent folder for output
OUTPUT_FILE = f'{os.path.splitext(FILE)[0]}.resize_{SENT_NUM}.txt'

all_sents = []

with open(FILE, 'r') as file:
    sentence = []
    lines = file.readlines()
    for line in lines:
        if re.search(r'(^\%\%)', line): continue
        sentence.append(line)
        if line == '\n':
            all_sents.append(sentence)
            sentence = []
            
out_sents = all_sents[:SENT_NUM]

if os.path.exists(OUTPUT_FILE):
  os.remove(OUTPUT_FILE)

with open(OUTPUT_FILE, 'a') as file:
    for sentence in out_sents:
        for token in sentence:
            file.write(token)


            
