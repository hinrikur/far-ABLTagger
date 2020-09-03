 
 
BIN_TAGS = ['KK-NFET', 'KK-ÞFET', 'KK-ÞGFET', 'KK-EFET', 'KK-NFFT', 'KK-ÞFFT', 
            'KK-ÞGFFT', 'KK-EFFT', 'KVK-NFET', 'KVK-ÞFET', 'KVK-ÞGFET', 
            'KVK-EFET', 'KVK-NFFT', 'KVK-ÞFFT', 'KVK-ÞGFFT', 'KVK-EFFT', 
            'HK-NFET', 'HK-ÞFET', 'HK-ÞGFET', 'HK-EFET', 'HK-NFFT', 'HK-ÞFFT', 
            'HK-ÞGFFT', 'HK-EFFT',]

ENDINGS = ['i', 'a', 'a', 'a', 'u', 'u', 'u', 'u', 'a', 'u', 'u', 'u', 'u', 
            'u', 'u', 'u', 'a', 'a', 'a', 'a', 'u', 'u', 'u', 'u',]

ENDINGS_2 = ['i', 'ja', 'ja', 'ja', 'ju', 'ju', 'ju', 'ju', 'ja', 'ju', 'ju', 'ju', 'ju', 
            'ju', 'ju', 'ju', 'ja', 'ja', 'ja', 'ja', 'ju', 'ju', 'ju', 'ju',]

INFL_DICT = dict(zip(BIN_TAGS, ENDINGS))
INFL_DICT_2 =  dict(zip(BIN_TAGS, ENDINGS_2))

def inflect(word, id):
    form_list = []
    if word.endswith('ndi'):
        # pass
        stem = word[:-1]
        for tag, ending in INFL_DICT.items():
            # print(';'.join([word, id, 'rt', 'manual', stem+ending, tag]))
            form_list.append(';'.join([word, id, 'rt', 'obg-gen', stem+ending, tag]))
    elif word in {'triði'}:
        # pass
        stem = word[:-1]
        for tag, ending in INFL_DICT_2.items():
            # print(';'.join([word, id, 'rt', 'manual', stem+ending, tag]))
            form_list.append(';'.join([word, id, 'rt', 'obg-gen', stem+ending, tag]))
    else:
        stem = word[:-1]
        for tag, ending in INFL_DICT.items():
            # print(';'.join([word, id, 'rt', 'manual', stem+ending, tag]))
            form_list.append(';'.join([word, id, 'rt', 'obg-gen', stem+ending, tag]))
    return form_list

if __name__ == '__main__':
    
    uninflected = 'FO_inflection_data/generated_paradigms/uninflected/rt.tsv'
    output = 'FO_inflection_data/SH_snid_output/sprotin_rt.txt'
    
    inflected_words = []
    
    with open(uninflected, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split('\t')
            id = line[1]
            word = line[0]
            forms = inflect(word, id)
            inflected_words.append(forms)
            # input()
    with open(output, 'w') as output:
        for word in inflected_words:
            for line in word:
                output.write(line)
                output.write('\n')
            output.write('\n')
