import os
import sys
from collections import defaultdict

"""
Script for extracting specific lemmas from UniMorph .tsv language file
"""

# python3 get_paradigms_from_UM.py FO_inflection_data/UniMorph/UM-non-sprotin_lemmas.txt FO_inflection_data/UniMorph/faroese.txt

# verandi;164892;lo;alm;verandi;FSB-KK-NFET
# verandi;164892;lo;alm;verandi;FSB-KK-ÞFET
# verandi;164892;lo;alm;verandi;FSB-KK-ÞGFET
# verandi;164892;lo;alm;verandi;FSB-KK-EFET
# verandi;164892;lo;alm;verandi;FSB-KK-NFFT
# verandi;164892;lo;alm;verandi;FSB-KK-ÞFFT
# verandi;164892;lo;alm;verandi;FSB-KK-ÞGFFT
# verandi;164892;lo;alm;verandi;FSB-KK-EFFT
# verandi;164892;lo;alm;verandi;FSB-KVK-NFET
# verandi;164892;lo;alm;verandi;FSB-KVK-ÞFET
# verandi;164892;lo;alm;verandi;FSB-KVK-ÞGFET
# verandi;164892;lo;alm;verandi;FSB-KVK-EFET
# verandi;164892;lo;alm;verandi;FSB-KVK-NFFT
# verandi;164892;lo;alm;verandi;FSB-KVK-ÞFFT
# verandi;164892;lo;alm;verandi;FSB-KVK-ÞGFFT
# verandi;164892;lo;alm;verandi;FSB-KVK-EFFT
# verandi;164892;lo;alm;verandi;FSB-HK-NFET
# verandi;164892;lo;alm;verandi;FSB-HK-ÞFET
# verandi;164892;lo;alm;verandi;FSB-HK-ÞGFET
# verandi;164892;lo;alm;verandi;FSB-HK-EFET
# verandi;164892;lo;alm;verandi;FSB-HK-NFFT
# verandi;164892;lo;alm;verandi;FSB-HK-ÞFFT
# verandi;164892;lo;alm;verandi;FSB-HK-ÞGFFT
# verandi;164892;lo;alm;verandi;FSB-HK-EFFT
# verandi;164892;lo;alm;verandi;FVB-KK-NFET
# verandi;164892;lo;alm;verandi;FVB-KK-ÞFET
# verandi;164892;lo;alm;verandi;FVB-KK-ÞGFET
# verandi;164892;lo;alm;verandi;FVB-KK-EFET
# verandi;164892;lo;alm;verandi;FVB-KK-NFFT
# verandi;164892;lo;alm;verandi;FVB-KK-ÞFFT
# verandi;164892;lo;alm;verandi;FVB-KK-ÞGFFT
# verandi;164892;lo;alm;verandi;FVB-KK-EFFT
# verandi;164892;lo;alm;verandi;FVB-KVK-NFET
# verandi;164892;lo;alm;verandi;FVB-KVK-ÞFET
# verandi;164892;lo;alm;verandi;FVB-KVK-ÞGFET
# verandi;164892;lo;alm;verandi;FVB-KVK-EFET
# verandi;164892;lo;alm;verandi;FVB-KVK-NFFT
# verandi;164892;lo;alm;verandi;FVB-KVK-ÞFFT
# verandi;164892;lo;alm;verandi;FVB-KVK-ÞGFFT
# verandi;164892;lo;alm;verandi;FVB-KVK-EFFT
# verandi;164892;lo;alm;verandi;FVB-HK-NFET
# verandi;164892;lo;alm;verandi;FVB-HK-ÞFET
# verandi;164892;lo;alm;verandi;FVB-HK-ÞGFET
# verandi;164892;lo;alm;verandi;FVB-HK-EFET
# verandi;164892;lo;alm;verandi;FVB-HK-NFFT
# verandi;164892;lo;alm;verandi;FVB-HK-ÞFFT
# verandi;164892;lo;alm;verandi;FVB-HK-ÞGFFT
# verandi;164892;lo;alm;verandi;FVB-HK-EFFT



TAG_DICT = {'ADJ;ACC;FEM;SG ' : 'FSB-KVK-ÞFET', 
            'ADJ;FEM;PL' : 'FSB-KVK-', 
            'ADJ;ACC;MASC;PL' : 'FSB-KK', 
            'ADJ;NOM;MASC;PL' : 'FSB-KK-NFFT', 
            'ADJ;GEN;FEM;SG' : 'FSB-KVK-EFET', 
            'ADJ;ACC;MASC;SG' : 'FSB-KK-ÞFET', 
            'ADJ;NEUT;PL' : [], 
            'ADJ;NOM;MASC;SG' : 'FSB-KK-NFET', 
            'ADJ;GEN;MASC;PL' : 'FSB-KK-EFET', 
            'ADJ;NOM;NEUT;SG' : 'FSB-HK-NFET', 
            'ADJ;ACC;NEUT;SG' : 'FSB-HK-ÞFET', 
            'ADJ;DAT;NEUT;SG' : 'FSB-HK-ÞGFET', 
            'ADJ;NOM;FEM;SG' : 'FSB-KVK-NFET', 
            'ADJ;GEN;MASC;SG' : 'FSB-KK-EFET', 
            'ADJ;DAT;FEM;SG' : 'FSB-KVK-ÞGFET', 
            'ADJ;DAT;MASC;PL' : 'FSB-KK', 
            'ADJ;DAT;MASC;SG' : 'FSB-KK-ÞGFET', 
            'ADJ;GEN;NEUT;SG' : 'FSB-HK-EFET', 
            'N;DEF;GEN;PL' : '',
            'N;DEF;ACC;SG' : '',
            'N;DEF;DAT;PL' : '',
            'N;INDF;ACC;PL' : '',
            'N;INDF;DAT;SG' : '',
            'N;INDF;ACC;SG' : '',
            'N;DEF;GEN;SG' : '',
            'N;INDF;NOM;SG' : '',
            'N;INDF;NOM;PL' : '',
            'N;INDF;DAT;PL' : '',
            'N;DEF;NOM;SG' : '',
            'N;INDF;GEN;SG' : '',
            'N;DEF;DAT;SG' : '',
            'N;DEF;ACC;PL' : '',
            'N;DEF;NOM;PL' : '',
            'N;INDF;GEN;PL' : '',
            'V;IMP;2;SG' : '',
            'V;IND;PST;3' : '',
            'V;IND;PRS;3;SG' : '',
            'V;IND;PRS;1;SG' : '',
            'V;IND;PRS;2;SG' : '',
            'V;IND;PST;3;SG' : '',
            'V.PTCP.PRS' : '',
            'V;NFIN' : '',
            'V;IMP;2;PL' : '',
            'V;IND;PRS;3' : '',
            'V;IND;PST;1;SG' : '',
            'V.CVB' : '',
            'V.PTCP.PST' : '',
            'V;IND;PST;2;SG' : ''}
        


def get_lemmas(file_handle):
    lemmas_classes = {}
    with open(file_handle) as file:
        for line in file.readlines():
            line = line.split('\t')
            lemmas_classes[line[0]] = line[1]
    return lemmas_classes

def get_paradigms(file_handle, lemma_class_dict):
    paradigms = defaultdict(list)
    with open(UniMorph_file) as file:
        for line in file.readlines():
            if line == '\n': continue
            line = line.strip('\n').split('\t')
            # print(line)
            tag_info = line[2].split(';')
            lemma = line[0]
            wclass = tag_info[0].lower()
            for lmm, wcls in lemma_class_dict.items():
                if lemma == lmm:
                    paradigms[lemma].append(line)
    return paradigms

def to_SHsnid(paradigm_dict)
    pass
            
if __name__ == '__main__':

    lemma_file = sys.argv[1]
    UniMorph_file = sys.argv[2]
    
    lemmas_classes = get_lemmas(lemma_file)
    paradigms = get_paradigms(UniMorph_file, lemmas_classes)
    
