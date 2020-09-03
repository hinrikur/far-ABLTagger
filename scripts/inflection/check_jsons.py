import os
import csv
import json
import re
import sys
from pprint import pprint

# JSON_PATH = '../../FO_inflection_data/json' 

JSON_PATH = [os.path.join(sys.argv[1], file) for file in os.listdir(sys.argv[1])] if os.path.isdir(sys.argv[1]) else [sys.argv[1]]

def get_json(file):
    sprotin_file = open(file, 'r')
    json_file = json.load(sprotin_file)
    return json_file

def get_word_info(word):
    # flex_cats = ' if word['InflexCats'][0] != '' else None
    # print(word['DisplayWord'])
    word_info = '\t'.join([
                        word['DisplayWord'],
                        str(word['Id']),
                        ';'.join(word['InflexCats']),
                        str(len(word['InflectedForm'])) if word['InflectedForm'] else '0'
                        # ';'.join(word['InflectedForm']) if word['InflectedForm'] else '',
                        ])
    return word_info

def write_tsv(fh, l):
    with open(fh+'.tsv', 'w') as f:
        for i in l:
            f.write(i)
            f.write('\n')
            
            
for file in JSON_PATH:
    if not file.endswith('.json'): continue
    inflected_words = 0
    json_object = get_json(file)
    for word in json_object['words']:
        if word['InflectedForm'] is not None:
            inflected_words += 1
    print(file, inflected_words)


# print(len(json['words']))

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

# flex_cats = set()
# for word in json['words']:
#     flex_cats.add(''.join(word['InflexCats']))
# for i in list(flex_cats):
#     print(i)



    # pprint(word)
    # input()
    # if word['DisplayWord'] == 'seta':
    #   pprint(word)
    # if '100' in word['InflexCats']:
    #     print(word['DisplayWord'], ''.join(word['InflexCats']))
    # if word['InflectedForm'] == None:
    #     print(get_word_info(word))

# word_info = []
# for word in json['words']:
#     print(get_word_info(word))
    # word_info.append(get_word_info(word))

# write_tsv(sys.argv[1], word_info)
    # pprint(word)
