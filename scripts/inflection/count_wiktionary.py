import os
import json
import sys
import re

"""
Script for counting lemmas in wiktionary json file
"""

def reformat_json_string(stuff):
    stuff = re.sub(r'\n}', '\n},', stuff)
    stuff = '[' + stuff[:-2] + ']'
    # stuff = stuff.split('\n\n')
    # print(stuff[:5000])
    return stuff
    
    
def lemmas_from_json(stuff, w_class):
    
    # lists for sorting words with head attr.
    has_heads = []
    has_no_heads = []
    
    # lists for sorting lemmas from word forms
    lemmas = []
    forms = []
    unknowns = []
        
    for word in stuff:
        if not word.get('heads'):
            has_no_heads.append(word)
        else:
            has_heads.append(word)
        # print(word.get('heads', word['word']))
        # input()
    
    print('With "heads":', len(has_heads))
    print('No "heads":', len(has_no_heads))
    print()
    
    for word in has_heads:
        word['class'] = w_class
        if not word['heads'][0].get('2'):
            lemmas.append(word)
        # elif word['heads'][0]['2'] in {'adjective form', 'adjective forms'}:
        elif re.search(r'forms?', word['heads'][0]['2']):
            forms.append(word)
        else:
            lemmas.append(word)
    
    print('Lemmas:', len(lemmas))
    print('Word forms:', len(forms))
    
    return lemmas

if __name__ == '__main__':
    
    # string constants
    IN_PATH = sys.argv[1]
    FILES = os.listdir(IN_PATH)
    OUT_FILE = os.path.join(IN_PATH, 'wikt-lemmas.txt')
    
    # lemma lists declared
    lemmas = []
    all_lemmas = []
    
    for file in FILES:
        # non-json files removed
        if not file.endswith('.json'): continue
        # file name printed to ouput
        print('\n\nCurrent file:', file)
        # filepath and word class saved as strings
        in_path = os.path.join(IN_PATH, file)
        w_class = file.replace('.json', '')
        # contents of file read as json and lemmas extracted
        with open(in_path, 'r') as in_file:
            data = in_file.read()
            new_data = reformat_json_string(data)
            json_data = json.loads(new_data)
            lemmas = lemmas_from_json(json_data, w_class)
            all_lemmas.extend(lemmas)
    
    print('\n\nTotal lemmas:', len(all_lemmas))
    
    with open(OUT_FILE, 'w') as file:
        for lemma in all_lemmas:
            lemma_str, class_str = lemma['word'], lemma['class']
            file.write(f'{lemma_str}\t{class_str}')
            file.write('\n')
    
    
