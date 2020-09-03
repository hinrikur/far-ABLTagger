import sys
# import argparse
import random
import re
import os
from shutil import rmtree



def main():
    # '../corpora/tagged_corpus_sosialurin/sosialurin_corpus_IStag.txt'
    FILE = sys.argv[1]
    FOLD = int(sys.argv[2])

    parent_folder = os.path.dirname(FILE)

    curr_fold = 1
    sent_counter = 0

    all_sents = []

    with open(FILE, 'r') as file:
        sentence = []
        lines = file.readlines()
        for line in lines:
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
        os.mkdir(f'{parent_folder}/{FOLD}_fold')
    except FileExistsError:
        rmtree(f'{parent_folder}/{FOLD}_fold')
        os.mkdir(f'{parent_folder}/{FOLD}_fold')

    for sentence in all_sents:
        sent_counter += 1
        if curr_fold == FOLD:
            with open(f'{parent_folder}/{FOLD}_fold/{curr_fold:02d}.txt', 'a') as file:
                for token in sentence:
                    file.write(token)
                # file.write('\n')
        elif sent_counter == part_sent_num:
            curr_fold += 1
            sent_counter = 0
            with open(f'{parent_folder}/{FOLD}_fold/{curr_fold:02d}.txt', 'a') as file:
                for token in sentence:
                    file.write(token)
                # file.write('\n')
        else:
            with open(f'{parent_folder}/{FOLD}_fold/{curr_fold:02d}.txt', 'a') as file:
                for token in sentence:
                    file.write(token)
                # file.write('\n')

if __name__ == '__main__':
    main()
