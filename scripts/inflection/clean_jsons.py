import os
import csv
import json
import re
import sys
from pprint import pprint
from collections import defaultdict

# HTML = re.compile(r'(\<\/*.*\>(?=[a-z])|\<\/*.*\>(?=\d)|<\/.*>|:)')
HTML = re.compile(r'<[^>]*>')

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

def cleaned_cat(str):
    str = re.sub('(\(.*\)|-s |\:)', '', str)
    str = re.split(r'( |  |/)', str)[0]
    return str

def clean_filename(str):
    str = re.sub('ð', 'd', str)
    str = re.sub('á', 'a', str)
    str = re.sub('ó', 'o', str)
    return str

if __name__ == '__main__':
    
        
    if not sys.argv[1]:
        exit()
        
    dict_name = sys.argv[1]
    
    JSON_PATH = '../FO_inflection_data/json/'+dict_name

    if not os.path.isdir(JSON_PATH):
        os.mkdir(JSON_PATH)
    
    JSON_FILES = all_jsons('../utils/sprotin.fo/data/'+dict_name)

    categories = defaultdict(int)
    cat_words = defaultdict(lambda: defaultdict(list))

    for word in JSON_FILES:
        word['InflexCats'] = re.sub(HTML, '', str(word['InflexCats']))
        word['InflexCats'] = re.sub('^ ', '', str(word['InflexCats']))
        word['InflexCats'] = re.split(r'(\d+)', word['InflexCats'])
        word['Explanation'] = re.sub(HTML, '', word['Explanation'])
        # if re.match(r'kv', word['InflexCats'][0]):
        #     word['InflexCats'] = word['InflexCats'][0].replace(word['InflexCats'][0], 'v', 1)
        # print(word['InflexCats'])
        categories[word['InflexCats'][0]] += 1
        cat_words[cleaned_cat(word['InflexCats'][0])]['words'].append(word)

    print(cat_words.keys())

    for category, words in cat_words.items():
        print(f'Currently writing {clean_filename(category)}.json')
        with open(os.path.join(JSON_PATH, f'{clean_filename(category)}.json'), 'a+') as f:
            json.dump(words, f,  ensure_ascii=False, indent=4)
