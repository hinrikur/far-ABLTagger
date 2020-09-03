

wclass_map = {'N': 'no', 'V': 'so', 'ADJ': 'lo'}

tag_map = {'ADJ;ACC;FEM;SG'     : 'KVK-ÞFET',
           'ADJ;ACC;MASC;PL'    : 'KK-ÞFFT',
           'ADJ;ACC;MASC;SG'    : 'KK-ÞFET',
           'ADJ;DAT;FEM;SG'     : 'KVK-ÞGFET',
           'ADJ;DAT;MASC;PL'    : 'KK-ÞGFFT',
           'ADJ;DAT;MASC;SG'    : 'KK-ÞGFET',
           'ADJ;DAT;NEUT;SG'    : 'HK-ÞGFET',
           'ADJ;NOM;FEM;PL'     : 'KVK-NFFT',
           'ADJ;ACC;FEM;PL'     : 'KVK-ÞFFT',
           'ADJ;DAT;FEM;PL'     : 'KVK-ÞGFFT',
           'ADJ;GEN;FEM;PL'     : 'KVK-EFFT',
           'ADJ;GEN;FEM;SG'     : 'KVK-EFET',
           'ADJ;GEN;MASC;PL'    : 'KK-EFFT',
           'ADJ;GEN;MASC;SG'    : 'KK-EFET',
           'ADJ;GEN;NEUT;SG'    : 'HK-EFET',
           'ADJ;NOM;NEUT;PL'    : 'HK-NFFT',
           'ADJ;ACC;NEUT;PL'    : 'HK-ÞFFT',
           'ADJ;DAT;NEUT;PL'    : 'HK-ÞGFFT',
           'ADJ;GEN;NEUT;PL'    : 'HK-EFFT',
           'ADJ;NOM;NEUT;SG'    : 'HK-NFET',
           'ADJ;ACC;NEUT;SG'    : 'HK-ÞFET',
           'ADJ;NOM;FEM;SG'     : 'KVK-NFET',
           'ADJ;NOM;MASC;PL'    : 'KK-NFFT',
           'ADJ;NOM;MASC;SG'    : 'KK-NFET',
           'N;DEF;ACC;PL'       : 'ÞFFTgr',
           'N;DEF;ACC;SG'       : 'ÞFETgr',
           'N;DEF;DAT;PL'       : 'ÞGFFTgr',
           'N;DEF;DAT;SG'       : 'ÞGFETgr',
           'N;DEF;GEN;PL'       : 'EFFTgr',
           'N;DEF;GEN;SG'       : 'EFETgr',
           'N;DEF;NOM;PL'       : 'NFFTgr',
           'N;DEF;NOM;SG'       : 'NFETgr',
           'N;INDF;ACC;PL'      : 'ÞFFT',
           'N;INDF;ACC;SG'      : 'ÞFET',
           'N;INDF;DAT;PL'      : 'ÞGFFT',
           'N;INDF;DAT;SG'      : 'ÞGFET',
           'N;INDF;GEN;PL'      : 'EFFT',
           'N;INDF;GEN;SG'      : 'EFET',
           'N;INDF;NOM;PL'      : 'NFFT',
           'N;INDF;NOM;SG'      : 'NFET',
           'V.CVB'              : 'GM-SAGNB', # LH ÞT (sagnbot)
           'V.PTCP.PRS'         : 'LH-NT', # LH NT
           'V.PTCP.PST'         : 'LHÞT-SB-KK-NFET', # LH ÞT
           'V;IMP;2;PL'         : 'GM-BH-FT',
           'V;IMP;2;SG'         : 'GM-BH-ET',
           'V;IND;PRS;1;SG'     : 'GM-FH-NT-1P-ET',
           'V;IND;PRS;2;SG'     : 'GM-FH-NT-2P-ET',
           'V;IND;PRS;3'        : 'GM-FH-NT-3P-FT',
           'V;IND;PRS;2'        : 'GM-FH-NT-2P-FT',
           'V;IND;PRS;1'        : 'GM-FH-NT-1P-FT',
           'V;IND;PRS;3;SG'     : 'GM-FH-NT-3P-ET',
           'V;IND;PST;1;SG'     : 'GM-FH-ÞT-1P-ET',
           'V;IND;PST;2;SG'     : 'GM-FH-ÞT-2P-ET',
           'V;IND;PST;3'        : 'GM-FH-ÞT-3P-FT',
           'V;IND;PST;2'        : 'GM-FH-ÞT-2P-FT',
           'V;IND;PST;1'        : 'GM-FH-ÞT-1P-FT',
           'V;IND;PST;3;SG'     : 'GM-FH-ÞT-3P-ET',
           'V;NFIN'             : 'GM-NH',}





def um_from_file(file_handle):
    all_words = []
    word = []
    with open(file_handle, 'r') as file:
        for line in file.readlines():
            if line.strip() == '':
                if len(word) > 0:
                    all_words.append(word)
                word = []
            else:
                word.append(line.strip('\n').split('\t'))
    return all_words

def lemmas_from_file(file_handle):
    all_words = {}
    with open(file_handle, 'r') as file:
        for line in file.readlines():
            pair = line.strip('\n').split('\t')
            all_words[pair[0]] = pair[1]
    return all_words

def multiply_forms(word_list):
    for word in word_list:
        for form in word:
            if form[2] == 'ADJ;NOM/ACC;NEUT;SG':
                form[2] = 'ADJ;NOM;NEUT;SG'
                word.append([form[0], form[1], 'ADJ;ACC;NEUT;SG'])
            elif form[2] == 'V;IND;PRS;3':
                word.append([form[0], form[1], 'V;IND;PRS;2'])
                word.append([form[0], form[1], 'V;IND;PRS;1'])
            elif form[2] == 'V;IND;PST;3':
                word.append([form[0], form[1], 'V;IND;PST;2'])
                word.append([form[0], form[1], 'V;IND;PST;1'])
            elif form[2] == 'ADJ;FEM;PL':
                form[2] = 'ADJ;NOM;FEM;SG'
                word.append([form[0], form[1], 'ADJ;ACC;FEM;PL'])
                word.append([form[0], form[1], 'ADJ;DAT;FEM;PL'])
                word.append([form[0], form[1], 'ADJ;GEN;FEM;PL'])
            elif form[2] == 'ADJ;NEUT;PL':
                form[2] = 'ADJ;NOM;NEUT;SG'
                word.append([form[0], form[1], 'ADJ;ACC;NEUT;PL'])
                word.append([form[0], form[1], 'ADJ;DAT;NEUT;PL'])
                word.append([form[0], form[1], 'ADJ;GEN;NEUT;PL'])
            
    return word_list

def convert_to_SH(word_list):
    new_list = []
    for word in word_list:
        new_word = []
        for form in word:
            wclass = form[2].replace('.', ';').split(';')[0]
            form = [form[0],'',wclass_map[wclass],'wiktionary', form[1], tag_map[form[2]]]
            new_word.append(form)
        new_list.append(new_word)
    return new_list

if __name__ == '__main__':
    
    fo_unimorph_file = um_from_file('FO_inflection_data/UniMorph/faroese.txt')
    needed_lemmas = lemmas_from_file('FO_inflection_data/UniMorph/applicable_lemmas.txt')
    
    needed_forms = []
    
    for word in fo_unimorph_file:
        if word[0][0] in needed_lemmas.keys():
            # print(word[0][0])
            needed_forms.append(word)
            
    print('Number of applicable forms:', len(needed_forms))
            
    needed_forms = multiply_forms(needed_forms)
    
    adj_list  = []
    noun_list = []
    verb_list = []
    
    for word in needed_forms:
        if word[0][2].replace('.', ';').split(';')[0] == 'ADJ':
            adj_list.append(word)
        elif word[0][2].replace('.', ';').split(';')[0] == 'N':
            noun_list.append(word)
        elif word[0][2].replace('.', ';').split(';')[0] == 'V':
            verb_list.append(word)
    
    adj_SH  = convert_to_SH(adj_list)
    noun_SH = convert_to_SH(noun_list)
    verb_SH = convert_to_SH(verb_list)
    
    
    
    with open('FO_inflection_data/SH_snid_output/unimorph_l', 'w') as file:
        for word in adj_SH:
            for form in word:
                file.write(';'.join(form))
                file.write('\n')
            file.write('\n')
    
    with open('FO_inflection_data/SH_snid_output/unimorph_n', 'w') as file:
        for word in noun_SH:
            for form in word:
                file.write(';'.join(form))
                file.write('\n')
            file.write('\n')
    
    with open('FO_inflection_data/SH_snid_output/unimorph_s', 'w') as file:
        for word in verb_SH:
            for form in word:
                file.write(';'.join(form))
                file.write('\n')
            file.write('\n')
