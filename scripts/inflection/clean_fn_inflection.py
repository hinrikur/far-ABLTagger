import os
import csv
import json
import re
import sys
from pprint import pprint
from collections import defaultdict

# HTML = re.compile(r'(\<\/*.*\>(?=[a-z])|\<\/*.*\>(?=\d)|<\/.*>|:)')
HTML = re.compile(r'<[^>]*>')
JUNK = re.compile(r'(\(?<[^>]*>~?\)?|\(?[æa-zðA-Z]+\.|bending|sí|flt|[0-9]+|\\[rn]|hv[sn]f)')

def get_json(file):
    sprotin_file = open(file, 'r')
    json_file = json.load(sprotin_file)
    return json_file

def all_jsons(dir):
    all_jsons = os.walk(dir)
    for x, y, files in all_jsons:
        for file in files:
            tree = get_json(os.path.join(dir, file))
            # pprint(tree['words'])
            for word in tree['words']:
                yield word

def cleaned_cat(string):
    string = re.sub('(\(.*\)|-s |\:)', '', string)
    string = re.split(r'( |  |/)', string)[0]
    return string

def clean_filename(string):
    string = re.sub('ð', 'd', string)
    string = re.sub('á', 'a', string)
    string = re.sub('ó', 'o', string)
    return string

def clean_simpleflex(string):
    if isinstance(string, str):
        string = re.sub(JUNK, '', string)
        string = re.sub(r'\s+', ' ', string)
        return string
    else:
        return '-'
if __name__ == '__main__':
    
    IN_FILE = OUT_FILE = None
    
    if not sys.argv[1]:
        exit()
        
    IN_FILE = sys.argv[1]
    if not len(sys.argv) < 3:
        OUT_FILE = sys.argv[2]
    
    data = get_json(IN_FILE)
        
    with open(OUT_FILE) if OUT_FILE else sys.stdout as output:
        for word in data['words']:
            string = word['DisplayWord'] + '\t' + clean_simpleflex(word['ShortInflectedForm'])
            output.write(string)
            output.write('\n')
        
    
    # JSON_PATH = '../FO_inflection_data/json/'+dict_name

    # if not os.path.isdir(JSON_PATH):
    #     os.mkdir(JSON_PATH)
    
    # JSON_FILES = all_jsons('../utils/sprotin.fo/data/'+dict_name)

    # categories = defaultdict(int)
    # cat_words = defaultdict(lambda: defaultdict(list))

    # for word in JSON_FILES:
    #     word['InflexCats'] = re.sub(HTML, '', str(word['InflexCats']))
    #     word['InflexCats'] = re.sub('^ ', '', str(word['InflexCats']))
    #     word['InflexCats'] = re.split(r'(\d+)', word['InflexCats'])
    #     word['Explanation'] = re.sub(HTML, '', word['Explanation'])
    #     # if re.match(r'kv', word['InflexCats'][0]):
    #     #     word['InflexCats'] = word['InflexCats'][0].replace(word['InflexCats'][0], 'v', 1)
    #     # print(word['InflexCats'])
    #     categories[word['InflexCats'][0]] += 1
    #     cat_words[cleaned_cat(word['InflexCats'][0])]['words'].append(word)
    # 
    # print(cat_words.keys())
    # 
    # for category, words in cat_words.items():
    #     print(f'Currently writing {clean_filename(category)}.json')
    #     with open(os.path.join(JSON_PATH, f'{clean_filename(category)}.json'), 'a+') as f:
    #         json.dump(words, f,  ensure_ascii=False, indent=4)
