import sys
import re

single_errors = {
                'fýra\tNONPD': 'fýra\tNCNPD', 
                'tíggju\tNOMPD': 'tíggju\tNCMPD',
                'fyrstur\tNOMSN': 'fyrstur\tASSMSN',
                'næstur\tNOMSN': 'næstur\tASSMSN'
                 }

def fix_single_errors(token_tag):
    try:
        token_tag = single_errors[token_tag]
        return token_tag
    except KeyError:
        return token_tag

def get_corpus(file_path):
    file_lines = []
    try:
        with open(file_path, 'r') as file:
            for line in file.readlines():
                line = [i for i in fix_single_errors(line.strip('\n')).split('\t')]
                file_lines.append(line)
        return file_lines
    except:
        print('Something went wrong when reading file:')
        raise
    
if __name__ == '__main__':
    CORPUS_PATH = sys.argv[1]
    corpus = get_corpus(CORPUS_PATH)
    
    for i in range(len(corpus)):
        if len(corpus[i]) < 2:
            continue
        elif corpus[i][1].startswith('P'):
            print(corpus[i])
