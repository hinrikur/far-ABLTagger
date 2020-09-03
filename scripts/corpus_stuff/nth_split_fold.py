import sys
# import argparse
import random
import re
import os
from shutil import rmtree
from collections import defaultdict

def write_to_file(lst, parent_folder, fold, name):
    for filename, sentences in lst.items():
        with open(f'{parent_folder}/{fold}_fold_{name}/{filename}.txt', 'a') as file:
            for sentence in sentences:
                for token in sentence:
                    file.write(token)

def main():
    # '../corpora/tagged_corpus_sosialurin/sosialurin_corpus_IStag.txt'
    FILE = sys.argv[1] # input tagged corpus
    SPLIT_NO = int(sys.argv[2]) # number of folds
    NAME = sys.argv[3] # name to add to output folder name
    SPLIT_NUMS = list(range(SPLIT_NO)) # each split number via range
    out_test_lists = defaultdict(list) # test sentence container
    out_train_lists = defaultdict(list) # train sentence container
    parent_folder = os.path.dirname(FILE)+'/processed/' # parent folder for output
    all_sents = [] # container for all input sentences
    
    print('No. of folds:', SPLIT_NO)
    print('Writing to folder:', parent_folder)

    with open(FILE, 'r') as file:
        sentence = []
        lines = file.readlines()
        for line in lines:
            if re.search(r'(^\%\%)', line): continue
            sentence.append(line)
            if line == '\n':
                all_sents.append(sentence)
                sentence = []

    total_sent_num = len(all_sents) # number of sentences
    sent_lengths = [len(i) for i in all_sents] # number of tokens per sentence

    print(f'\nTotal number of sentences: {total_sent_num}')
    print(f'Total number of tokens: {sum(sent_lengths)}\n')
    
    # make output directory parent folder
    try:
        os.mkdir(parent_folder)
    except FileExistsError:
        pass
    
    # make output directory
    try:
        os.mkdir(f'{parent_folder}/{SPLIT_NO}_fold_{NAME}')
    except FileExistsError:
        rmtree(f'{parent_folder}/{SPLIT_NO}_fold_{NAME}')
        os.mkdir(f'{parent_folder}/{SPLIT_NO}_fold_{NAME}')
    
    # extract nth sentence
    split_dest = 0 # counter for split loop
    for sentence in all_sents:
        test_split_name = f'{(split_dest+1):02d}PM'
        out_test_lists[test_split_name].append(sentence)
        split_dest += 1
        if split_dest == SPLIT_NO:
            split_dest = 0

    for i in SPLIT_NUMS:
        train_split_name = f'{(i+1):02d}TM'
        test_split_name = f'{(i+1):02d}PM'
        for k,v in out_test_lists.items():
            if k == test_split_name:
                continue
            else:
                out_train_lists[train_split_name].extend(v) 

    write_to_file(out_test_lists, parent_folder, SPLIT_NO, NAME)
    write_to_file(out_train_lists, parent_folder, SPLIT_NO, NAME)

    

if __name__ == '__main__':
    main()
