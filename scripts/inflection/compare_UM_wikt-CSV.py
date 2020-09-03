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
    WIKT_IN = sys.argv[2]
    
    morph_lemmas = [] # list of lemmas in additional morphology file
    wikt_lemmas = set() # set of lemmas in json file
    
    # lemmas from UniMorph file gathered
    with open(MORPH_IN, 'r') as file:
        for line in file.readlines():
            morph_lemmas.append(line.split('\t')[0].strip().lower())
    
    # Lemmas from Wiktionary lemma file gathered
    with open(WIKT_IN, 'r') as file:
        for line in file.readlines():
            # lemma = line.split('\t')[0]
            if line.split('\t')[1].strip() in {'verb', 'noun', 'adj'}:
                wikt_lemmas.add(line.strip().lower())
    
    # size of lemma list printed to output
    print('No. of lemmas in wikt:', len(wikt_lemmas))
    print('No. of lemmas in UniMorph file:', len(morph_lemmas))
    print('No. of extra lemmas in WIktionary file:', len(wikt_lemmas)-len(morph_lemmas))
    
    print('\nLemmas not in UniMorph data:\n')
    
    
    for line in wikt_lemmas:
        lemma = line.split('\t')[0]
        if lemma not in morph_lemmas:
            print(line)
