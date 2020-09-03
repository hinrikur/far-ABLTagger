
import os
import json
import sys
import re
import argparse
from pprint import pprint

from generate_verb_forms import * # temp import all, only import needed

"""
Script for generating SHsnid type .csv output from inflection data
extracted from Sprotin.fo dictionary, in json format
"""

VERB_PARADIGM_DICT = get_paradigms('FO_inflection_data/hj/verb_suffixes.tsv', 'dict')

NOM_CATS = ['NFET', 'ÞFET', 'ÞGFET', 'EFET', 'NFFT', 'ÞFFT', 'ÞGFFT', 'EFFT', 
            'NFETgr', 'ÞFETgr', 'ÞGFETgr', 'EFETgr', 'NFFTgr', 'ÞFFTgr', 
            'ÞGFFTgr', 'EFFTgr']
PRP_CATS = ['NFET', 'ÞFET', 'ÞGFET', 'EFET', 'NFFT', 'ÞFFT', 'ÞGFFT', 'EFFT',]
VERB_CATS = ['GM-NH',
             'GM-FH-NT-1P-ET', 'GM-FH-NT-2P-ET', 'GM-FH-NT-3P-ET', 
             'GM-FH-NT-1P-FT', 'GM-FH-NT-2P-FT', 'GM-FH-NT-3P-FT', 
             'GM-FH-ÞT-1P-ET', 'GM-FH-ÞT-2P-ET', 'GM-FH-ÞT-3P-ET', 
             'GM-FH-ÞT-1P-FT', 'GM-FH-ÞT-2P-FT', 'GM-FH-ÞT-3P-FT', 
             'GM-VH-NT-1P-ET', 'GM-VH-NT-2P-ET', 'GM-VH-NT-3P-ET', 
             'GM-VH-NT-1P-FT', 'GM-VH-NT-2P-FT', 'GM-VH-NT-3P-FT', 
             'GM-VH-ÞT-1P-ET', 'GM-VH-ÞT-2P-ET', 'GM-VH-ÞT-3P-ET', 
             'GM-VH-ÞT-1P-FT', 'GM-VH-ÞT-2P-FT', 'GM-VH-ÞT-3P-FT',
             'MM-NH', 
             'MM-FH-NT-1P-ET', 'MM-FH-NT-2P-ET', 'MM-FH-NT-3P-ET', 
             'MM-FH-NT-1P-FT', 'MM-FH-NT-2P-FT', 'MM-FH-NT-3P-FT', 
             'MM-FH-ÞT-1P-ET', 'MM-FH-ÞT-2P-ET', 'MM-FH-ÞT-3P-ET', 
             'MM-FH-ÞT-1P-FT', 'MM-FH-ÞT-2P-FT', 'MM-FH-ÞT-3P-FT', 
             'MM-VH-NT-1P-ET', 'MM-VH-NT-2P-ET', 'MM-VH-NT-3P-ET', 
             'MM-VH-NT-1P-FT', 'MM-VH-NT-2P-FT', 'MM-VH-NT-3P-FT', 
             'MM-VH-ÞT-1P-ET', 'MM-VH-ÞT-2P-ET', 'MM-VH-ÞT-3P-ET', 
             'MM-VH-ÞT-1P-FT', 'MM-VH-ÞT-2P-FT', 'MM-VH-ÞT-3P-FT', 
             'GM-BH-ST', 'GM-BH-ET', 'GM-BH-FT', 
             'LH-NT', 
             'GM-SAGNB', 
             'MM-SAGNB']
VERB_PP_ST = ['LHÞT-SB-KK-NFET', 'LHÞT-SB-KK-ÞFET','LHÞT-SB-KK-ÞGFET', 'LHÞT-SB-KK-EFET', 
              'LHÞT-SB-KK-NFFT', 'LHÞT-SB-KK-ÞFFT', 'LHÞT-SB-KK-ÞGFFT', 'LHÞT-SB-KK-EFFT', 
              'LHÞT-SB-KVK-NFET', 'LHÞT-SB-KVK-ÞFET', 'LHÞT-SB-KVK-ÞGFET', 'LHÞT-SB-KVK-EFET', 
              'LHÞT-SB-KVK-NFFT', 'LHÞT-SB-KVK-ÞFFT', 'LHÞT-SB-KVK-ÞGFFT', 'LHÞT-SB-KVK-EFFT', 
              'LHÞT-SB-HK-NFET', 'LHÞT-SB-HK-ÞFET', 'LHÞT-SB-HK-ÞGFET', 'LHÞT-SB-HK-EFET', 
              'LHÞT-SB-HK-NFFT', 'LHÞT-SB-HK-ÞFFT', 'LHÞT-SB-HK-ÞGFFT', 'LHÞT-SB-HK-EFFT',] 
VERB_PP_WK = ['LHÞT-VB-KK-NFET', 'LHÞT-VB-KK-ÞFET', 'LHÞT-VB-KK-ÞGFET', 'LHÞT-VB-KK-EFET', 
              'LHÞT-VB-KK-NFFT', 'LHÞT-VB-KK-ÞFFT', 'LHÞT-VB-KK-ÞGFFT', 'LHÞT-VB-KK-EFFT', 
              'LHÞT-VB-KVK-NFET', 'LHÞT-VB-KVK-ÞFET', 'LHÞT-VB-KVK-ÞGFET', 'LHÞT-VB-KVK-EFET', 
              'LHÞT-VB-KVK-NFFT', 'LHÞT-VB-KVK-ÞFFT', 'LHÞT-VB-KVK-ÞGFFT', 'LHÞT-VB-KVK-EFFT', 
              'LHÞT-VB-HK-NFET', 'LHÞT-VB-HK-ÞFET', 'LHÞT-VB-HK-ÞGFET', 'LHÞT-VB-HK-EFET', 
              'LHÞT-VB-HK-NFFT', 'LHÞT-VB-HK-ÞFFT', 'LHÞT-VB-HK-ÞGFFT', 'LHÞT-VB-HK-EFFT',] 
ADJ_POS_ST = ['FSB-KK-NFET', 'FSB-KK-ÞFET', 'FSB-KK-ÞGFET', 'FSB-KK-EFET', 
              'FSB-KK-NFFT', 'FSB-KK-ÞFFT', 'FSB-KK-ÞGFFT', 'FSB-KK-EFFT',
              'FSB-KVK-NFET', 'FSB-KVK-ÞFET', 'FSB-KVK-ÞGFET', 'FSB-KVK-EFET',
              'FSB-KVK-NFFT','FSB-KVK-ÞFFT','FSB-KVK-ÞGFFT','FSB-KVK-EFFT',
              'FSB-HK-NFET','FSB-HK-ÞFET','FSB-HK-ÞGFET','FSB-HK-EFET',
              'FSB-HK-NFFT','FSB-HK-ÞFFT','FSB-HK-ÞGFFT','FSB-HK-EFFT',]
ADJ_POS_WK = ['FVB-KK-NFET','FVB-KK-ÞFET','FVB-KK-ÞGFET','FVB-KK-EFET',
              'FVB-KK-NFFT','FVB-KK-ÞFFT','FVB-KK-ÞGFFT','FVB-KK-EFFT',
              'FVB-KVK-NFET','FVB-KVK-ÞFET','FVB-KVK-ÞGFET','FVB-KVK-EFET',
              'FVB-KVK-NFFT', 'FVB-KVK-ÞFFT','FVB-KVK-ÞGFFT','FVB-KVK-EFFT',
              'FVB-HK-NFET','FVB-HK-ÞFET', 'FVB-HK-ÞGFET','FVB-HK-EFET',
              'FVB-HK-NFFT','FVB-HK-ÞFFT','FVB-HK-ÞGFFT', 'FVB-HK-EFFT',]
ADJ_COM = ['MST-KK-NFET','MST-KK-ÞFET','MST-KK-ÞGFET','MST-KK-EFET',
           'MST-KK-NFFT','MST-KK-ÞFFT','MST-KK-ÞGFFT','MST-KK-EFFT',
           'MST-KVK-NFET', 'MST-KVK-ÞFET','MST-KVK-ÞGFET','MST-KVK-EFET',
           'MST-KVK-NFFT','MST-KVK-ÞFFT', 'MST-KVK-ÞGFFT','MST-KVK-EFFT',
           'MST-HK-NFET','MST-HK-ÞFET','MST-HK-ÞGFET', 'MST-HK-EFET',
           'MST-HK-NFFT','MST-HK-ÞFFT','MST-HK-ÞGFFT','MST-HK-EFFT']
ADJ_SUP_ST = ['ESB-KK-NFET','ESB-KK-ÞFET','ESB-KK-ÞGFET','ESB-KK-EFET',
              'ESB-KK-NFFT','ESB-KK-ÞFFT','ESB-KK-ÞGFFT','ESB-KK-EFFT',
              'ESB-KVK-NFET', 'ESB-KVK-ÞFET','ESB-KVK-ÞGFET','ESB-KVK-EFET',
              'ESB-KVK-NFFT', 'ESB-KVK-ÞFFT', 'ESB-KVK-ÞGFFT','ESB-KVK-EFFT',
              'ESB-HK-NFET','ESB-HK-ÞFET', 'ESB-HK-ÞGFET', 'ESB-HK-EFET',
              'ESB-HK-NFFT','ESB-HK-ÞFFT','ESB-HK-ÞGFFT', 'ESB-HK-EFFT']
ADJ_SUP_WK = ['EVB-KK-NFET','EVB-KK-ÞFET','EVB-KK-ÞGFET','EVB-KK-EFET',
              'EVB-KK-NFFT', 'EVB-KK-ÞFFT', 'EVB-KK-ÞGFFT','EVB-KK-EFFT',
              'EVB-KVK-NFET', 'EVB-KVK-ÞFET','EVB-KVK-ÞGFET', 'EVB-KVK-EFET',
              'EVB-KVK-NFFT', 'EVB-KVK-ÞFFT','EVB-KVK-ÞGFFT','EVB-KVK-EFFT', 
              'EVB-HK-NFET', 'EVB-HK-ÞFET','EVB-HK-ÞGFET','EVB-HK-EFET',
              'EVB-HK-NFFT',  'EVB-HK-ÞFFT','EVB-HK-ÞGFFT','EVB-HK-EFFT',]

ADJ_POS_WK_ENDS = ['i', 'a', 'a', 'a', # masc. sing.
                   'u', 'u', 'u', 'u', # masc. pl.
                   'a', 'u', 'u', 'u', # fem. sing.
                   'u', 'u', 'u', 'u', # fem. pl.
                   'a', 'a', 'a', 'a', # fem. sing.
                   'u', 'u', 'u', 'u'] # fem. pl.


def get_json(file):
    sprotin_file = open(file, 'r')
    json_file = json.load(sprotin_file)
    return json_file

def inflect_adj(stem, suffix):
    if suffix == 'u':
        pass
    else:
        form = stem + suffix
    return form 

def verb_SHsnid_strings(forms, word_id, word_cat):
    SH_snid_strings = [] # output
    SH_tagstrings = [] # strings from VERB_CATS to use
    pp_form = None # past participle form given in json
    if len(forms) == 15:
        SH_tagstrings = VERB_CATS[:13] + VERB_CATS[-5:-1] + ['GM-VH']
        # print(forms)
        forms = forms[:4] + [forms[4]]*3 + forms[5:8] + [forms[8]]*3 + forms[9:12] + [ forms[13], forms[14]]
        pp_form = forms[12]
        # print(forms)
    elif len(forms) > 15:
        # print(forms)
        SH_tagstrings = VERB_CATS[:13] + VERB_CATS[25:38] + VERB_CATS[-5:-1]
        middle_forms = forms[15:19] + [forms[19]]*3 + forms[20:23] + [forms[23]]*3 
        forms = forms[:4] + [forms[4]]*3 + forms[5:8] + [forms[8]]*3 + middle_forms + forms[9:12] + [ forms[13], forms[14]]
        # print(forms)
        # pp_form = forms[12]

    for form_tag_pair in zip(forms, SH_tagstrings):
        if '/' in form_tag_pair[0]:
            SH_snid_strings.append([forms[0], word_id, 
                                    word_cat, 'obg-gen', 
                                    form_tag_pair[0].split('/')[0], 
                                    form_tag_pair[1]])
            SH_snid_strings.append([forms[0], word_id, 
                                    word_cat, 'obg-gen', 
                                    form_tag_pair[0].split('/')[1], 
                                    form_tag_pair[1]+'2'])
        else:
            SH_snid_strings.append([forms[0], word_id, 
                                    word_cat, 'obg-gen', 
                                    form_tag_pair[0], form_tag_pair[1]])
    if pp_form:
        SH_snid_strings.append([forms[0], word_id, 
                                word_cat, 'obg-gen', 
                                pp_form, 'LHÞT'])
    # # DEBUG:
    # for i in SH_snid_strings:
    #     print(i)  
    return SH_snid_strings

# NOUN SHsnid example:

# 'afarorð;428750;hk;alm;afarorð;NFET'
# 'afarorð;428750;hk;alm;afarorðið;NFETgr'
# 'afarorð;428750;hk;alm;afarorð;ÞFET'
# 'afarorð;428750;hk;alm;afarorðið;ÞFETgr'
# 'afarorð;428750;hk;alm;afarorði;ÞGFET'
# 'afarorð;428750;hk;alm;afarorðinu;ÞGFETgr'
# 'afarorð;428750;hk;alm;afarorðs;EFET'
# 'afarorð;428750;hk;alm;afarorðsins;EFETgr'
# 'afarorð;428750;hk;alm;afarorð;NFFT'
# 'afarorð;428750;hk;alm;afarorðin;NFFTgr'
# 'afarorð;428750;hk;alm;afarorð;ÞFFT'
# 'afarorð;428750;hk;alm;afarorðin;ÞFFTgr'
# 'afarorð;428750;hk;alm;afarorðum;ÞGFFT'
# 'afarorð;428750;hk;alm;afarorðunum;ÞGFFTgr'
# 'afarorð;428750;hk;alm;afarorða;EFFT'
# 'afarorð;428750;hk;alm;afarorðanna;EFFTgr'

# VERB SHsnid example: (double comments not used)

# skapa;422870;so;alm;skapa;GM-NH
# skapa;422870;so;alm;skapa;GM-FH-NT-1P-ET
# skapa;422870;so;alm;skapar;GM-FH-NT-2P-ET
# skapa;422870;so;alm;skapar;GM-FH-NT-3P-ET
# skapa;422870;so;alm;sköpum;GM-FH-NT-1P-FT
# skapa;422870;so;alm;skapið;GM-FH-NT-2P-FT
# skapa;422870;so;alm;skapa;GM-FH-NT-3P-FT
# skapa;422870;so;alm;skapaði;GM-FH-ÞT-1P-ET
# skapa;422870;so;alm;skapaðir;GM-FH-ÞT-2P-ET
# skapa;422870;so;alm;skapaði;GM-FH-ÞT-3P-ET
# skapa;422870;so;alm;sköpuðum;GM-FH-ÞT-1P-FT
# skapa;422870;so;alm;sköpuðuð;GM-FH-ÞT-2P-FT
# skapa;422870;so;alm;sköpuðu;GM-FH-ÞT-3P-FT
# skapa;422870;so;alm;skapi;GM-VH-NT-1P-ET
# # skapa;422870;so;alm;skapir;GM-VH-NT-2P-ET
# # skapa;422870;so;alm;skapi;GM-VH-NT-3P-ET
# # skapa;422870;so;alm;sköpum;GM-VH-NT-1P-FT
# # skapa;422870;so;alm;skapið;GM-VH-NT-2P-FT
# # skapa;422870;so;alm;skapi;GM-VH-NT-3P-FT
# # skapa;422870;so;alm;skapaði;GM-VH-ÞT-1P-ET
# # skapa;422870;so;alm;skapaðir;GM-VH-ÞT-2P-ET
# # skapa;422870;so;alm;skapaði;GM-VH-ÞT-3P-ET
# # skapa;422870;so;alm;sköpuðum;GM-VH-ÞT-1P-FT
# # skapa;422870;so;alm;sköpuðuð;GM-VH-ÞT-2P-FT
# # skapa;422870;so;alm;sköpuðu;GM-VH-ÞT-3P-FT
# skapa;422870;so;alm;skapast;MM-NH
# skapa;422870;so;alm;skapast;MM-FH-NT-1P-ET
# skapa;422870;so;alm;skapast;MM-FH-NT-2P-ET
# skapa;422870;so;alm;skapast;MM-FH-NT-3P-ET
# skapa;422870;so;alm;sköpumst;MM-FH-NT-1P-FT
# skapa;422870;so;alm;skapist;MM-FH-NT-2P-FT
# skapa;422870;so;alm;skapast;MM-FH-NT-3P-FT
# skapa;422870;so;alm;skapaðist;MM-FH-ÞT-1P-ET
# skapa;422870;so;alm;skapaðist;MM-FH-ÞT-2P-ET
# skapa;422870;so;alm;skapaðist;MM-FH-ÞT-3P-ET
# skapa;422870;so;alm;sköpuðumst;MM-FH-ÞT-1P-FT
# skapa;422870;so;alm;sköpuðust;MM-FH-ÞT-2P-FT
# skapa;422870;so;alm;sköpuðust;MM-FH-ÞT-3P-FT
# skapa;422870;so;alm;skapist;MM-VH-NT-1P-ET
# # skapa;422870;so;alm;skapist;MM-VH-NT-2P-ET
# # skapa;422870;so;alm;skapist;MM-VH-NT-3P-ET
# # skapa;422870;so;alm;sköpumst;MM-VH-NT-1P-FT
# # skapa;422870;so;alm;skapist;MM-VH-NT-2P-FT
# # skapa;422870;so;alm;skapist;MM-VH-NT-3P-FT
# # skapa;422870;so;alm;skapaðist;MM-VH-ÞT-1P-ET
# # skapa;422870;so;alm;skapaðist;MM-VH-ÞT-2P-ET
# # skapa;422870;so;alm;skapaðist;MM-VH-ÞT-3P-ET
# # skapa;422870;so;alm;sköpuðumst;MM-VH-ÞT-1P-FT
# # skapa;422870;so;alm;sköpuðust;MM-VH-ÞT-2P-FT
# # skapa;422870;so;alm;sköpuðust;MM-VH-ÞT-3P-FT
# skapa;422870;so;alm;skapa;GM-BH-ST
# skapa;422870;so;alm;skapaðu;GM-BH-ET
# skapa;422870;so;alm;skapið;GM-BH-FT
# skapa;422870;so;alm;skapandi;LH-NT
# skapa;422870;so;alm;skapað;GM-SAGNB
# skapa;422870;so;alm;skapast;MM-SAGNB

# skapa;422870;so;alm;skapaður;LHÞT-SB-KK-NFET
# skapa;422870;so;alm;skapaðan;LHÞT-SB-KK-ÞFET
# skapa;422870;so;alm;sköpuðum;LHÞT-SB-KK-ÞGFET
# skapa;422870;so;alm;skapaðs;LHÞT-SB-KK-EFET
# skapa;422870;so;alm;skapaðir;LHÞT-SB-KK-NFFT
# skapa;422870;so;alm;skapaða;LHÞT-SB-KK-ÞFFT
# skapa;422870;so;alm;sköpuðum;LHÞT-SB-KK-ÞGFFT
# skapa;422870;so;alm;skapaðra;LHÞT-SB-KK-EFFT
# skapa;422870;so;alm;sköpuð;LHÞT-SB-KVK-NFET
# skapa;422870;so;alm;skapaða;LHÞT-SB-KVK-ÞFET
# skapa;422870;so;alm;skapaðri;LHÞT-SB-KVK-ÞGFET
# skapa;422870;so;alm;skapaðrar;LHÞT-SB-KVK-EFET
# skapa;422870;so;alm;skapaðar;LHÞT-SB-KVK-NFFT
# skapa;422870;so;alm;skapaðar;LHÞT-SB-KVK-ÞFFT
# skapa;422870;so;alm;sköpuðum;LHÞT-SB-KVK-ÞGFFT
# skapa;422870;so;alm;skapaðra;LHÞT-SB-KVK-EFFT
# skapa;422870;so;alm;skapað;LHÞT-SB-HK-NFET
# skapa;422870;so;alm;skapað;LHÞT-SB-HK-ÞFET
# skapa;422870;so;alm;sköpuðu;LHÞT-SB-HK-ÞGFET
# skapa;422870;so;alm;skapaðs;LHÞT-SB-HK-EFET
# skapa;422870;so;alm;sköpuð;LHÞT-SB-HK-NFFT
# skapa;422870;so;alm;sköpuð;LHÞT-SB-HK-ÞFFT
# skapa;422870;so;alm;sköpuðum;LHÞT-SB-HK-ÞGFFT
# skapa;422870;so;alm;skapaðra;LHÞT-SB-HK-EFFT
# skapa;422870;so;alm;skapaði;LHÞT-VB-KK-NFET
# skapa;422870;so;alm;skapaða;LHÞT-VB-KK-ÞFET
# skapa;422870;so;alm;skapaða;LHÞT-VB-KK-ÞGFET
# skapa;422870;so;alm;skapaða;LHÞT-VB-KK-EFET
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KK-NFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KK-ÞFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KK-ÞGFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KK-EFFT
# skapa;422870;so;alm;skapaða;LHÞT-VB-KVK-NFET
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KVK-ÞFET
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KVK-ÞGFET
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KVK-EFET
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KVK-NFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KVK-ÞFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KVK-ÞGFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-KVK-EFFT
# skapa;422870;so;alm;skapaða;LHÞT-VB-HK-NFET
# skapa;422870;so;alm;skapaða;LHÞT-VB-HK-ÞFET
# skapa;422870;so;alm;skapaða;LHÞT-VB-HK-ÞGFET
# skapa;422870;so;alm;skapaða;LHÞT-VB-HK-EFET
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-HK-NFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-HK-ÞFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-HK-ÞGFFT
# skapa;422870;so;alm;sköpuðu;LHÞT-VB-HK-EFFT

def clean_category(cat):
    class_regex = r'(kv-n|k-n|kv|k|hj|h|lh|l|fs|sb|mðlv|s|sern|fn|ljóðh|kve|t|hvmf|n|flt|miðst|hást|kób|f|við|hvnf|boðsh|hób|hvsf|ób|kn)'
    # print(cat)
    if isinstance(cat, list):
        cat = cat[0]
        # cat = ' '.join(cat)
        # 
    if cat in {'kób', 'hób'}:
        return cat[0]
    elif cat == 'ób' or cat in {'h/k', 'h/kv', 'h:'}:
        return 'h'
    elif cat in {'hj/l', 'hj:'}:
        return 'hj'
    # print(cat)
    else:
        cat = re.search(class_regex, cat)
    # print(cat)
    return cat[0]

# def get_word_class(wclass_list_from_json):
#     return re.search(r'\d+', wclass_list_from_json)


def generate_SH(word_json):
    word_SH = []
    
    # Inflection category standardized
    CATEGORY = clean_category(word_json['InflexCats'])
    
    # adverbs
    if CATEGORY  in {'hj',}:
        word_SH = [[word_json['DisplayWord'], word_json['Id'], 
                    CATEGORY, 'obg', 
                    word_json['DisplayWord'], 'OBENDILIGT']]
        return word_SH
    
    # verbs
    if CATEGORY == 's':
        # string to return in case of error
        error_string = word_json['DisplayWord'] +'\nCause: No verb forms generated'
        # new forms generated from json data
        new_forms = generate_paradigms_json(VERB_PARADIGM_DICT, word_json)
        # # DEBUG:
        # input()
        # SHsnid string built from new generated forms
        word_SH = verb_SHsnid_strings(new_forms, word_json['Id'], CATEGORY) if new_forms else error_string
        return word_SH
    
    # nouns
    if CATEGORY in {'k', 'h', 'kv'}:
        if word_json['InflectedForm']:
            forms_tags = list(zip(word_json['InflectedForm'], NOM_CATS))
            for form_tag in forms_tags:
                if form_tag[0] == '-':
                    continue
                elif '/' in form_tag[0]:
                    word_SH.append([word_json['DisplayWord'], word_json['Id'], 
                                    CATEGORY, 'obg', 
                                    form_tag[0].split('/')[0], form_tag[1]])
                    word_SH.append([word_json['DisplayWord'], word_json['Id'], 
                                    CATEGORY, 'obg', 
                                    form_tag[0].split('/')[1],form_tag[1]+'2'])
                    
                else:
                    word_SH.append([word_json['DisplayWord'], word_json['Id'], 
                            CATEGORY, 'obg', 
                            form_tag[0], form_tag[1]])
                    
        # uninflected (apparently)        
        else:
            # print(word_json['DisplayWord'], 'No inflected forms')
            word_SH = [[word_json['DisplayWord'], word_json['Id'], 
                        CATEGORY, 'obg', 
                        word_json['DisplayWord'], 'OBENDILIGT']]
        return word_SH
        
    # proper names
    elif CATEGORY in {'k-n', 'kv-n'}:
        if word_json['Explanation']:
            # forms saved to list
            infl_forms = re.sub(r'\[.*\]', '', word_json['Explanation']).strip('()*')
            # fixing escaped letters
            infl_forms = re.sub(r'&aacute;', 'á', infl_forms)
            infl_forms = re.sub(r'&yacute;', 'ý', infl_forms)
            infl_forms = re.sub(r'&oacute;', 'ó', infl_forms)
            # lemma inserted into word form list
            infl_forms = infl_forms.split(',')
            infl_forms.insert(0, word_json['DisplayWord'])
            forms_tags = list(zip(infl_forms, NOM_CATS))
            for form_tag in forms_tags:
                if form_tag[0] == '-':
                    continue
                elif '/' in form_tag[0]:
                    word_SH.append([word_json['DisplayWord'], '', word_json['InflexCats'][0], 'malrad', 
                                    form_tag[0].split('/')[0].strip(), form_tag[1]])
                    word_SH.append([word_json['DisplayWord'], '', word_json['InflexCats'][0], 'malrad', 
                                    form_tag[0].split('/')[1].strip(),form_tag[1]+'2'])
                else:
                    word_SH.append([word_json['DisplayWord'], '', word_json['InflexCats'][0], 'malrad', 
                                    form_tag[0].strip(),form_tag[1]])
        # uninflected (apparently, although this should not be expected from 
        # proper nouns but kept in case)
        else:
            word_SH = [[word_json['DisplayWord'], '', word_json['InflexCats'][0], 'malrad', 
                        word_json['DisplayWord'].strip(),'OBENDILIGT']]
        return word_SH
        
    # adjectives
    elif CATEGORY in {'l','lh'}:
        if word_json['InflectedForm']:
            adj_stem = re.sub(r'ur$', '', word_json['DisplayWord'])
            forms_tags = list(zip(word_json['InflectedForm'], ADJ_POS_ST))
            pos_wk_ends_tags = list(zip(ADJ_POS_WK_ENDS, ADJ_POS_WK))
            for form_tag in forms_tags:
                if form_tag[0] == '-':
                    continue
                # catches alternate form 
                elif '/' in form_tag[0]:
                    word_SH.append([word_json['DisplayWord'], word_json['Id'], 
                                    CATEGORY, 'obg', 
                                    form_tag[0].split('/')[0], form_tag[1]])
                    word_SH.append([word_json['DisplayWord'], word_json['Id'], 
                                    CATEGORY, 'obg', 
                                    form_tag[0].split('/')[1], form_tag[1]+'2'])
                # only one form
                else:
                    word_SH.append([word_json['DisplayWord'], word_json['Id'], 
                                    CATEGORY, 'obg', 
                                    form_tag[0], form_tag[1]])
                    
            # generates positive definite form: stem + end
            # TODO: Find solution. Might not be possible / feasible
            # Commented out due to umlaut
            # for end_tag in pos_wk_ends_tags:
            #     word_SH.append([word_json['DisplayWord'], word_json['Id'], 
            #                     CATEGORY, 'obg', 
            #                     adj_stem+end_tag[0], end_tag[1]])
            
        # uninflected (apparently)
        else:
            word_SH = [[word_json['DisplayWord'], word_json['Id'], 
                        CATEGORY, 'obg', 
                        word_json['DisplayWord'], 'OBENDILIGT']]
        return word_SH
    # to catch word "heilagur" in flt.json (should be adjective)
    elif CATEGORY == 'flt' and word_json['DisplayWord'] == 'heilagur':
        if word_json['InflectedForm']:
            adj_stem = re.sub(r'ur$', '', word_json['DisplayWord'])
            forms_tags = list(zip(word_json['InflectedForm'], ADJ_POS_ST))
            pos_wk_ends_tags = list(zip(ADJ_POS_WK_ENDS, ADJ_POS_WK))
            for form_tag in forms_tags:
                word_SH.append([word_json['DisplayWord'], word_json['Id'], 
                                CATEGORY, 'obg', 
                                form_tag[0], form_tag[1]])
        else:
            word_SH = [[word_json['DisplayWord'], word_json['Id'], 
                        CATEGORY, 'obg', 
                        word_json['DisplayWord'], 'OBENDILIGT']]
        return word_SH
    else:
        return word_json['DisplayWord'] +'\nCause: wrong class'
        

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', help='path to output FOLDER')
    parser.add_argument('--verbose', '-v', help='flag for printing errors to stdout',
                        action='store_true')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--input', '-i', nargs='+', required=True, 
                               default=argparse.SUPPRESS, help='')

    args = parser.parse_args()
    
    # JSON_PATH = './FO_inflection_data/json'
    # SH_PATH =  './FO_inflection_data/SH_snid'
    # CLASS_FILE = sys.argv[1]
    # json = get_json(os.path.join(JSON_PATH, CLASS_FILE+'.json'))
    
    # output folder created if missing
    if args.output and not os.path.isdir(args.output):
        os.mkdir(args.output)
    
    for file_path in args.input:
        
        # other files / dirs filtered out
        if not file_path.endswith('.json'):
            continue
        
        # paths created
        JSON_PATH = file_path
        FILE_NAME = os.path.basename(JSON_PATH)
        output_file = os.path.join(args.output, FILE_NAME) if args.output else None
        
        print(f'Processing inflection data from file: {JSON_PATH}')
        print(f'Output JSON location: {output_file}\n')
        
        # JSON data read from file
        data = get_json(JSON_PATH)
        
        # SH data added to each word JSON and rewritten at new location
        with open(output_file, 'w') if output_file else sys.stdout as output:
            for word in data['words']:
                SH = generate_SH(word)
                # print(SH)
                # pprint(word)
                # input()
                if isinstance(SH, str) and args.verbose:
                    print("Error:")
                    print(SH+'\n')
                    print('Json not processsed:')
                    print()
                    pprint(word)
                    print()
                    input('Press enter to continue')
                    continue
                if not isinstance(SH, str):
                    word['SH'] = SH
                # for i in SH:
                #     output.write(';'.join([str(j) for j in i])+'\n')
                if not output_file:
                    json.dump(word, output,  ensure_ascii=False, indent=4)
                    input()
            if output_file:        
                json.dump(data, output,  ensure_ascii=False, indent=4)
            
    print('All done!')
