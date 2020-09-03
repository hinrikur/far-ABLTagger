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
    
    SPROT_IN = sys.argv[1]
    OTHER_IN = sys.argv[2]
    
    sprotin_lemmas = set() # set of lemmas in sprotin
    other_lemmas = [] # list of lemmas from other sources
    
    # lemmas from UniMorph file gathered
    with open(SPROT_IN, 'r') as file:
        for line in file.readlines():
            sprotin_lemmas.add(line.split(';')[0].strip().lower())
    
    # Lemmas from Wiktionary lemma file gathered
    with open(OTHER_IN, 'r') as file:
        for line in file.readlines():
            # lemma = line.split('\t')[0]
            other_lemmas.append(line.strip().lower())
    
    # size of lemma list printed to output
    print('No. of lemmas in Sprotin file:', len(sprotin_lemmas))
    print('No. of lemmas in Wiktionary / UniMorph:', len(other_lemmas))
    # print('No. of extra lemmas in WIktionary file:', len(sprotin_lemmas)-len(other_lemmas))
    
    # list declared for missing lemmas
    total_missing_lemmas = []
    
    for line in other_lemmas:
        lemma = line.split('\t')[0].lower()
        if lemma not in sprotin_lemmas:
            if line.split('\t')[1].strip() in {'verb', 'noun', 'adj', 'n', 'v','ADJ', 'N', 'V',}:
                print(line)
                total_missing_lemmas.append(line)
    
    print('\nNo. lemmas not in Sprotin data:', len(total_missing_lemmas))    

    # with open('FO_inflection_data/non_sprotin_lemmas.txt', 'w') as file:
    #     for lemma in total_missing_lemmas:
    #         # lemma = line.split('\t')[0]
    #         file.write(lemma)
    #         file.write('\n')
