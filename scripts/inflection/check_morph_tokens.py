import sys
from string import punctuation

if __name__ == '__main__':
    
    # corpus_file = 'corpora/tagged_corpus_sosialurin/fo.revised.txt'
    corpus_file = sys.argv[1]
    FO_morph_file = 'FO_inflection_data/SH_snid_output/COMBINED_TEST.csv'
    output_file = 'corpora/unkown_morph_tokens.txt'
    
    corpus_set = set()
    word_form_set = set()
    missing_tokens = []
    
    with open(corpus_file, 'r') as file:
        lines  = file.readlines()
        for line in lines:
            if line.split('\t')[0] not in punctuation:
                corpus_set.add(line)
    
    print('Number of corpus word forms:', len(corpus_set))
    
            
    with open(FO_morph_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            word_form = line.split(';')[4].lower()
            word_form_set.add(word_form)

    print('Number of morph word forms:', len(word_form_set))

    for pair in corpus_set:
        if isinstance(pair, list) and pair.split('\t')[0].lower() not in word_form_set:
            missing_tokens.append(pair)
        elif isinstance(pair, str) and pair.lower().strip() not in word_form_set:
            missing_tokens.append(pair)
    
    print('Number of forms not in morph data:', len(missing_tokens))

    with open(output_file, 'w') as file:
        for pair in missing_tokens:
            file.write(pair)
            # file.write('\n')
        
