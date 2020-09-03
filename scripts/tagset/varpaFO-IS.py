#!/usr/bin/env python3
import subprocess

''' ========================= '''
'''     Variables defined     '''
''' ========================= '''



# debug variables for testing
'''
no_tags = ['SFSNP', 'SXP', 'SNSDL', 'SNPN', 'SMSNA', 'SMPN', 'SNPN', 'SFSN', 'SFSNA', 'SFSDP', 'SNSDL', 'SMSDL']
lo_tags = ['APSFSN', 'APSNSN', 'APWFSA', 'APSMPA', 'APWMSD', 'APSFSA', 'APSNSA', 'APSFSN']
pfn_tags = [ 'P1SA', 'P1SN', 'P2SD', 'P1SD', 'PDFSA', 'PDFSA', 'PDFSN', 'PDNPD', 'PDNPA', 'PDMPN', 'PINSN','PIMSA','PIFSN','PIMSA','PIMSN','PIMSD','PIMPA','PIFSD','PIFSA','PINSA', 'PFPG', 'PFPN', 'PFSA', 'PFSD', 'PFSG', 'PFSN']
to_tags = ['NOMSA', 'NCNPD', 'NC', 'NCMSA', 'NCFPA', 'NMPA']
so_tags = ['VNPS3', 'VNPS3', 'VNPS3', 'VNPS3', 'VNPS2', 'VNPS2', 'VNPS3', 'VNPS3', 'VA', 'VNAS3', 'VNAS3', 'VA', 'VI', 'VI', 'VNAS1', 'VAMPN']
ao_tags = ['DN', 'DCN', 'DSN', 'DCD']
st_tags = ['C', 'CR', 'CI']

combined_tags = no_tags + lo_tags + pfn_tags + to_tags + so_tags + ao_tags + st_tags
'''

word_class = { # All word classes used in tagset
    'S' : 'n', # nouns
    'A' : 'l', # adjectives
    'P' : 'f', # pronouns
    'N' : 't', # numerals
    'V' : 's', # verbs
    'D' : 'a', # adverbs
    'C' : 'c', # conjunctions
    'E' : 'a', # prepositions
    'I' : 'x', # interjection
    'F' : 'e', # foreign word
    'X' : 'x', # unanalyzed word
    'T' : 'as' # abbrevations
    }
gender = { # nouns, adjectives
    'F' : 'v', # femenine gender
    'M' : 'k', # masculine gender
    'N' : 'h', # neuter gender
    'X' : 'x'  # other/unspecified
    }
number = {
    'S' : 'e', # singular
    'P' : 'f'  # plural
    }
case = { # Nouns, adjectives, past participles
    'N' : 'n', # nominative
    'A' : 'o', # accusative
    'D' : 'þ', # dative
    'G' : 'e'  # genetive
    }
declension = { # Adjectives
    'S' : 's', # strong declension
    'W' : 'v', # week declension
    'I' : 'o'  # indeclinable
    }
degree = { # Adjectives, adverbs
    'P' : 'f', # positive
    'C' : 'm', # comparative
    'S' : 'e'  # superlative
    }
subcategory = { # pronouns
    'D' : 'a', # demonstrative pronoun
    'I' : 'b'  # indefinite demonstrative pronoun
    }
mood = {
    'I' : 'ng', # infinitive
    'M' : 'b',  # imperative
    'N' : 'fg', # indicative
    'S' : 'v',  # subjunctive
    'P' : 'l',  # present participle
    'E' : 'fm', # 'medium'
    'A' : 'þ'   # past participle
    }
tense = { # verbs
    'P' : 'n', # present tense
    'A' : 'þ'  # past tense
    }

category_case_governor = { # adverbs, prepositions
    'N' : 'a', # does not dominate case
    'A' : 'o', # dominates accusative
    'D' : 'þ', # dominates dative
    'G' : 'e'  # dominates genetive
    }
category_conj = { # conjunctions
    'I' : 'n', # infinitive marker 'at'
    'R' : 't'  # relative conjunction
    }
proper_nown = { # only proper nouns
    'P' : 's', # proper noun
    'L' : 's' # location (generalized 's' for icelandic)
    }

# lists for rearranging tags
adj_order = [0, 3, 4, 5, 2, 1]
vrb_order = [0, 1, 2, 5, 4, 3]
adv_order = [0, 2, 1]

# list / repostory for tags read from file
fo_tags = []
fo_words = []

''' ========================= '''
'''     Functions defined     '''
''' ========================= '''

def arrange(mark, order):
    '''
    Reorganizes charecters in a tag or string (obj 1) by order in list (obj 2)
    '''
    char_list = []
    for char in mark:
        char_list.append(char)
    char_list = [char_list[i] for i in order]
    mark = ''.join(char_list)
    return mark

def proc_noun(mark):
    '''
    Translates FO noun tags to IS noun tags
    Ex: SMSNA -> nkeng
    '''
    mark = mark.replace(mark[0], word_class[mark[0]], 1)
    mark = mark.replace(mark[1], gender[mark[1]], 1)
    if len(mark) == 2:
        return mark
    if len(mark) == 3:
        mark = mark.replace(mark[2], proper_nown[mark[2]], 1)
    if len(mark) > 3:
        mark = mark.replace(mark[2], number[mark[2]], 1)
        mark = mark.replace(mark[3], case[mark[3]], 1)
        mark = mark.replace('A', 'g', 1)
        mark = mark.replace('P', 'm', 1)
        mark = mark.replace('L', 'ö', 1)
        return mark
    return mark

def proc_adjective(mark):
    '''
    Translates FO adjective tags to IS adjective tags
    Ex: APSFSN -> lvensf
    '''
    mark = mark.replace(mark[0], word_class[mark[0]], 1)
    if len(mark) == 2:
        mark = mark.replace(mark[1], declension[mark[1]], 1)
        return mark
    else:
        mark = mark.replace(mark[1], degree[mark[1]], 1)
        mark = mark.replace(mark[2], declension[mark[2]], 1)
        mark = mark.replace(mark[3], gender[mark[3]], 1)
        mark = mark.replace(mark[4], number[mark[4]], 1)
        mark = mark.replace(mark[5], case[mark[5]], 1)
        return arrange(mark, adj_order)

def proc_pronoun(mark):
    '''
    Translates FO pronoun tags to IS pronoun tags
    note # generalizes 'a' tag for subcategory
    Ex: PDNSN -> fahen
    Ex: P1PN  -> fa1fn
    '''
    step = 0
    # print(mark)
    if len(mark) == 4:
        mark = 'f' + mark
        # step += 1
        # print('Step {0}: {1}'.format(step, mark))
        mark = mark.replace(mark[1], 'a', 1)
        # step += 1
        # print('Step {0}: {1}'.format(step, mark))
        mark = mark.replace(mark[3], number[mark[3]], 1)
        # step += 1
        # print('Step {0}: {1}'.format(step, mark))
        mark = mark.replace(mark[4], case[mark[4]], 1)
        # step += 1
        # print('Step {0}: {1}'.format(step, mark))
        try:
            mark = mark.replace(mark[2], gender[mark[2]], 1)
            # step += 1
            # print('Step {0}: {1}'.format(step, mark))
        except:
            pass
        return mark
    else:
        mark = mark.replace(mark[0], word_class[mark[0]], 1)
        mark = mark.replace(mark[1], subcategory[mark[1]], 1)
        mark = mark.replace(mark[2], gender[mark[2]], 1)
        mark = mark.replace(mark[3], number[mark[3]], 1)
        mark = mark.replace(mark[4], case[mark[4]], 1)
    return mark

def proc_numeral(mark):
    '''
    Translates FO numeral tags to IS numeral tags
    Ex: NOMSA -> takeo
    '''
    mark = mark.replace(mark[0], word_class[mark[0]], 1)
    if len(mark) == 2:
        mark = mark.replace(mark[1], 'a', 1)
        return mark
    elif len(mark) == 4:
        mark = mark.replace(mark[1], gender[mark[1]], 1)
        mark = mark.replace(mark[2], number[mark[2]], 1)
        mark = mark.replace(mark[3], case[mark[3]], 1)
        return mark
    elif len(mark) > 4:
        mark = mark.replace(mark[1], 'a', 1)
        mark = mark.replace(mark[2], gender[mark[2]], 1)
        mark = mark.replace(mark[3], number[mark[3]], 1)
        mark = mark.replace(mark[4], case[mark[4]], 1)
        return mark
    else:
        return mark

def proc_verb(mark):
    '''
    Translates FO verb tags to IS verb tags
    Ex: VNAS3 -> sfg3eþ
    Ex: VAFSN -> sþven (past participle)
    '''
    mark = mark.replace(mark[0], word_class[mark[0]], 1)
    mark = mark.replace(mark[1], mood[mark[1]], 1)
    if len(mark) == 3:
        if mark[2] in ('m', 'g'):
            return mark
        else:
            mark = mark.replace(mark[2], number[mark[2]], 1)
            return mark
    if len(mark) < 3:
        return mark
    else:
        if mark[1] == 'þ':
            mark = mark.replace(mark[2], gender[mark[2]], 1)
            mark = mark.replace(mark[3], number[mark[3]], 1)
            mark = mark.replace(mark[4], case[mark[4]], 1)
            return mark
        else:
            mark = mark.replace(mark[3], tense[mark[3]], 1)
            mark = mark.replace(mark[4], number[mark[4]], 1)
            return arrange(mark, vrb_order)

def proc_adverb(mark):
    '''
    Translates FO adverb AND PREPOSITION tags to IS adverb tags
    Ex: DN -> aa
    '''
    mark = mark.replace(mark[0], word_class[mark[0]], 1)
    if len(mark) == 2:
        mark = mark.replace(mark[1], category_case_governor[mark[1]], 1)
        return mark
    else:
        mark = mark.replace(mark[1], degree[mark[1]], 1)
        mark = mark.replace(mark[2], category_case_governor[mark[2]], 1)
        return arrange(mark, adv_order)

def proc_conjunction(mark):
    '''
    Translates FO conjunction tags to IS conjunction tags
    Ex: CR -> ct
    '''
    mark = mark.replace(mark[0], word_class[mark[0]], 1)
    if len(mark) == 1:
        return mark
    else:
        mark = mark.replace(mark[1], category_conj[mark[1]], 1)
    return mark

def proc_extra(mark):
    '''
    Translates any other FO tag to corresponding IS tag
    (should only take in uniletter tag)
    '''
    mark = mark.replace(mark[0], word_class[mark[0]], 1)

def translate_tag(tag):
    # out_list = []
    # teljari = 0
    # for tag in taglist:
    if tag[0] == 'S':
        # out_list.append([tag, proc_noun(tag)])
        tag = proc_noun(tag)
    elif tag[0] == 'A':
        # out_list.append([tag, proc_adjective(tag)])
        tag = proc_adjective(tag)
    elif tag[0] == 'P':
        # out_list.append([tag, proc_pronoun(tag)])
        tag = proc_pronoun(tag)
    elif tag[0] == 'N':
        # out_list.append([tag, proc_numeral(tag)])
        tag = proc_numeral(tag)
    elif tag[0] == 'V':
        # out_list.append([tag, proc_verb(tag)])
        tag = proc_verb(tag)
    elif tag[0] == 'D' or tag[0] == 'E':
        # out_list.append([tag, proc_adverb(tag)])
        tag = proc_adverb(tag)
    elif tag[0] == 'C':
        # out_list.append([tag, proc_conjunction(tag)])
        tag = proc_conjunction(tag)
    elif tag[0] not in word_class.keys():
        # out_list.append([tag, 'x'])
        tag = tag
    else:
        tag = tag.replace(tag[0], word_class[tag[0]], 1)
    # return out_list
    return tag


''' ========================= '''
'''       Functions run       '''
''' ========================= '''

# for tag in pfn_tags:
#     proctag = proc_pronoun(tag)
#     print(tag, proctag)

FO_corpus = open('../tagged_corpus_sosialurin/corpus.txt', 'r').readlines()
all_lines = [line.strip('\n').split('\t') for line in FO_corpus]
for line in all_lines:
    if len(line) == 2:
        line[1] = translate_tag(line[1])

# fo_is_taglist = translate_tag(fo_tags)

with open('../tagged_corpus_sosialurin/corpus_IStag.txt', 'w') as file:
    for pair in all_lines:
        if pair[0] == '.':
            file.write(pair[0] + '\t' + pair[0] + '\n')
            file.write('\n')
        elif len(pair) == 2:
            file.write(pair[0] + '\t' + pair[1] + '\n')


# split into test/train corpora
subprocess.call(['./split_TrainTest.sh'])
