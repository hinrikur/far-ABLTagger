import os
import csv
import json
import re
import sys
from pprint import pprint

JSON_PATH = 'FO_inflection_data/sprotin/json/fo-fo'

def get_json(file):
    sprotin_file = open(file, 'r')
    json_file = json.load(sprotin_file)
    return json_file

def write_tsv(fh, l):
    with open(fh+'.tsv', 'w') as f:
        for i in l:
            f.write('\t'.join(i))
            f.write('\n')

json = get_json(os.path.join(JSON_PATH, sys.argv[1]+'.json'))

# 'Id',
# 'SearchWord',
# 'DisplayWord',
# 'WordList',
# 'InflexCats',
# 'ShortInflectedForm',
# 'InflectedForm',
# 'Explanation',
# 'Origin',
# 'OriginSource',
# 'GrammarComment',
# 'WordNr',
# 'Index',w
# 'Phonetic',
# 'Date',
# 'ShortInflection'

lines = []

for word in json['words']:
    id = re.sub(r'(^s|:$)', '', ''.join(word['InflexCats']))
    lemma = word['DisplayWord']
    forms = word['InflectedForm'] if word['InflectedForm'] else []
    if '/' in id:
        id = id.split('/')
        # lines.append(f'{id[0]}\t{lemma}')
        # lines.append(f'{id[1]}\t{lemma}')
        lines.append([id[0], lemma]+forms)
        lines.append([id[1], lemma]+forms)
    elif id == '':
        lines.append(['999', lemma]+forms)
    else:
        lines.append(([id, lemma]+forms))

# duplicates removed and list sorted
lines = sorted([i for n, i in enumerate(lines) if i not in lines[:n]], key=lambda x: int(x[0]))

# print(len(lines))
# for i in lines:
#      print(i)

write_tsv('FO_inflection_data/generated_paradigms/uninflected/'+sys.argv[1], sorted(lines, key=lambda x: int(x[0])))
