import sys
import glob
import os

'''
script for counting sentences and tokens in tagged corpus
'''

# '../corpora/tagged_corpus_sosialurin/sosialurin_corpus_IStag.txt'
FILES = [os.path.join(sys.argv[1], file) for file in os.listdir(sys.argv[1])] if os.path.isdir(sys.argv[1]) else [sys.argv[1]]

# print(FILES)
if len(sys.argv) == 2:
    print(f'File \tsents\tno. tokens\ttoken-tag pairs\tunique tokens\tunique tags')

for file_name in FILES:
    if os.path.isdir(file_name): continue
    sent_count = 0
    token_count = 0
    
    uniq_lines = set()
    uniq_tokens = set()
    uniq_tags = set()
    
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line == '\n':
                sent_count += 1
            else:
                token_count += 1
                token_tag = line.strip('\n')
                token = token_tag.split('\t')[0]
                tag = token_tag.split('\t')[1]
                uniq_lines.add(token_tag)
                uniq_tokens.add(token)
                uniq_tags.add(tag)
                
                
    uniq_lines_count = len(uniq_lines)
    uniq_token_count = len(uniq_tokens)
    uniq_tags_count = len(uniq_tags)
                
    if len(sys.argv) == 2:
        print(f'{os.path.basename(file_name)}\t{sent_count}\t{token_count}\t{uniq_lines_count}\t{uniq_token_count}\t{uniq_tags_count}')
    elif sys.argv[2] == '-v':
        print(f'\nNo. of sents in {os.path.basename(file_name)}: {sent_count}')
        print(f'No. of tokens in {os.path.basename(file_name)}: {token_count}')
        print(f'\nNo. of unique token-tag pairs in {os.path.basename(file_name)}: {uniq_lines_count}')
        print(f'No. of unique tags in {os.path.basename(file_name)}: {uniq_token_count}')
        print(f'No. of unique tags in {os.path.basename(file_name)}: {uniq_tags_count}')
