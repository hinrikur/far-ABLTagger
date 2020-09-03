import os
import json
import sys

def get_json(file):
    sprotin_file = open(file, 'r')
    json_file = json.load(sprotin_file)
    return json_file

if __name__ == '__main__':
    
    # UniMorph lemma files:
    # FO_inflection_data/UniMorph/fo-lemmas-a.txt
    # FO_inflection_data/UniMorph/fo-lemmas-n.txt
    # FO_inflection_data/UniMorph/fo-lemmas-v.txt
    
    MORPH_IN = sys.argv[1]
    JSON_IN = sys.argv[2]
    
    morph_lemmas = [] # list of lemmas in additional morphology file
    json_lemmas = set() # set of lemmas in json file
    
    # lemmas from UniMorph file gathered
    with open(MORPH_IN, 'r') as file:
        for line in file.readlines():
            morph_lemmas.append(line.strip().lower())
    
    # Lemmas from JSON file gathered
    json_data = get_json(JSON_IN)
    for word in json_data['words']:
        json_lemmas.add(word['DisplayWord'].lower())
            
    print('No. of lemmas in json:', len(json_lemmas))
    print('No. of lemmas in UniMorph file:', len(morph_lemmas))
    
    print('\nLemmas not in Sprotin data:\n')
    
    for lemma in morph_lemmas:
        if lemma not in json_lemmas:
            print(lemma)
