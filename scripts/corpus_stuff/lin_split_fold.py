import sys
# import argparse
import random
import re
import os
from shutil import rmtree

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    # '../corpora/tagged_corpus_sosialurin/sosialurin_corpus_IStag.txt'
    FILE = sys.argv[1] # input tagged corpus
    FOLD = int(sys.argv[2]) # number of folds
    NAME = sys.argv[3] # name to add to output folder name
    
    print('No. of folds:', FOLD)
    
    parent_folder = os.path.dirname(FILE)+'/processed/'
    
    print('Writing to folder:', parent_folder)
    
    curr_fold = 0
    sent_counter = 0

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

    total_sent_num = len(all_sents)

    part_sent_num = int(round(total_sent_num/FOLD))

    print(f'\nTotal number of sentences: {total_sent_num}')
    sent_lengths = [len(i) for i in all_sents]
    print(f'Total number of tokens: {sum(sent_lengths)}\n')

    try:
        os.mkdir(f'{parent_folder}/{FOLD}_fold_{NAME}')
    except FileExistsError:
        rmtree(f'{parent_folder}/{FOLD}_fold_{NAME}')
        os.mkdir(f'{parent_folder}/{FOLD}_fold_{NAME}')

    n_folds = list(chunks(all_sents, part_sent_num))

    # for i in n_folds:
    #     print(len(i))

    if len(n_folds) == FOLD + 1:
        extra_sents = n_folds[-1]
        n_folds = n_folds[:-1]
        while len(extra_sents):
            for fold in n_folds:
                if len(extra_sents):
                    fold.append(extra_sents[0])
                    extra_sents.remove(extra_sents[0])

    # for i in n_folds:
    #     print(len(i))

    for fold in n_folds:
        curr_fold += 1
        fold_index = curr_fold - 1
        with open(f'{parent_folder}/{FOLD}_fold_{NAME}/{curr_fold:02d}PM.txt', 'a') as file:
            for sentence in fold:
                for token in sentence:
                    file.write(token)
        with open(f'{parent_folder}/{FOLD}_fold_{NAME}/{curr_fold:02d}TM.txt', 'a') as file:
            for fold in n_folds[:fold_index] + n_folds[curr_fold:]:
                for sentence in fold:
                    for token in sentence:
                        file.write(token)


if __name__ == '__main__':
    main()
