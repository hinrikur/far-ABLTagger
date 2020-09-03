import argparse
import os
import re
from sys import stdout

from string import punctuation


"""
Script for revising Faroese tagset of tagged corpus.
Based on tagged corpus Sosialurin

- Removes comments
- Fixes '...' tokens 
- Fixes ordinal numerical tokens where punctuation is seperated
- Adds newlines after EOS punctuation if missing
"""

# get cleaned corpus:
# python3 ./scripts/tagset/revise_FO_tags.py -c -n -i corpora/tagged_corpus_sosialurin/fo.txt -o corpora/tagged_corpus_sosialurin/fo.cleaned.txt
# python3 python3 ./scripts/corpus_stuff/check_double_sents.py -f -i corpora/tagged_corpus_sosialurin/fo.cleaned.txt -o corpora/tagged_corpus_sosialurin/fo.cleaned.txt

# get revised corpus:
# python3 ./scripts/tagset/revise_FO_tags.py -c -t -n -i corpora/tagged_corpus_sosialurin/fo.txt -o corpora/tagged_corpus_sosialurin/fo.revised.txt
# python3 ./scripts/corpus_stuff/check_double_sents.py -f -i corpora/tagged_corpus_sosialurin/fo.revised.txt -o corpora/tagged_corpus_sosialurin/fo.revised.txt

# get revised corpus, without 3p plural verb change:
# python3 ./scripts/tagset/revise_FO_tags.py -c -t -n -v -i corpora/tagged_corpus_sosialurin/fo.txt -o corpora/tagged_corpus_sosialurin/fo.revised-verbs-unchanged.txt
# 

# RegEx string to match ordinals except fyrsti (annar, triði, fjórði and possibly more) 
# numeral tag to be converted to adjective tag
ordinal_token = r'^(anna[nrð](s|ra)?|[aø]ðr(um?|ir)|onnur|triðj?(a|u|i)|fjórð[aiu]|.*[au]nd[ai])$'
# seperate regex to catch 'fyrsti/fyrstu/fyrsta', as it is always tagged  superlative
fyrsti_token = r'fyrst[aui]'

# End-of-sentence tokens to use in newline function
EOS_TOKENS = {'.', '?', '!', '...', '..', '....', '.....', '......' '«'}

# ordinal numeral tags converted to adjective tags
numeral_revisions_superlative = {
                                'NCFSA': 'ASWFSA',
                                'NONSD': 'ASWNSD',
                                'NOMSN': 'ASWMSN',
                                'NOFSN': 'ASWFSN',
                                'NONSA': 'ASWNSA',
                                'NCFPA': 'ASWFPA',
                                'NOMSD': 'ASWMSD',
                                'NOFSA': 'ASWFSA',
                                'NOMSA': 'ASWMSA',
                                'NOFSD': 'ASWFSD',
                                'NONPA': 'ASWNPA',
                                'NOMPD': 'ASWMPD',
                                'NONSN': 'ASWNSN',
                                }



numeral_revisions_positive = {
                            'NCFSA': 'APWFSA',
                            'NONSD': 'APWNSD',
                            'NOMSD': 'APWMSN',
                            'NOFSN': 'APWFSN',
                            'NONSA': 'APWNSA',
                            'NOMSN': 'APWMSN',
                            'NCFPA': 'APWFPA',
                            'NOFSA': 'APWFSA',
                            'NOMSA': 'APWMSA',
                            'N0FSA': 'APWFSA',
                            'NOFSD': 'APWFSD',
                            'NONPA': 'APWNPA',
                            'NOMPD': 'APWMPD',
                            'NONSN': 'APWNSN',
                            }

# general blanket revisions
single_revisions = {
                'SFSDL': 'SFSDP',
                'SFPAL': 'SFPAP',
                'SFPDAL': 'SFPDAP',
                'SFPDL': 'SFPDP',
                'SFPGL': 'SFPGP',
                'SFPNL': 'SFPNP',
                'SFSAAL': 'SFSAAP',
                'SFSAL': 'SFSAP',
                'SFSDAL': 'SFSDAP',
                'SFSDL': 'SFSDP',
                'SFSGL': 'SFSGP',
                'SFSNAL': 'SFSNAP',
                'SFSNL': 'SFSNP',
                'SMPDL': 'SMPDP',
                'SMSAL': 'SMSAP',
                'SMSDAL': 'SMSDAP',
                'SMSDL': 'SMSDP',
                'SMSGL': 'SMSGP',
                'SMSNL': 'SMSNP',
                'SNPDL': 'SNPDP',
                'SNPNL': 'SNPNP',
                'SNSAAL': 'SNSAAP',
                'SNSAL': 'SNSAP',
                'SNSDAL': 'SNSDAP',
                'SNSDL': 'SNSDP',
                'SNSGL': 'SNSGP',
                'SNSNAL': 'SNSNAP',
                'SNSNL': 'SNSNP',
                'SXL': 'SXP',
                'DA': 'DG',
                'DD': 'DG',
                'DCA': 'DCG',
                'DCD': 'DCG',
                'DSA': 'DSG',
                'DSD': 'DSG',
                'EN': 'DN',
                'EA': 'DG',
                'ED': 'DG',
                'EG': 'DG',
                'I': 'DI',
                # VA tag converted to VANSN (as done in MIM GOLD)
                'VA': 'VANSN',
                # Person removed from plural verbs
                'VEAP1': 'VEAP',
                'VEAP3': 'VEAP',
                'VEPP1': 'VEPP',
                'VEPP2': 'VEPP',
                'VEPP3': 'VEPP',
                'VNAP1': 'VNAP',
                'VNAP3': 'VNAP',
                'VNPP1': 'VNPP',
                'VNPP2': 'VNPP',
                'VNPP3': 'VNPP',
                # 'T': 'DT', # NOT REMOVED
                '!': 'KE', # punctuation EOS
                '"': 'KQ', # punctuation quotation 
                '#': 'KO', # punctuation 
                '$': 'M',  # symbol
                '%': 'M',  # symbol
                '&': 'M',  # symbol
                "'": 'KQ',
                '(': 'KO', # punctuation other
                ')': 'KO', # punctuation other
                '*': 'KO', # punctuation other
                '+': 'M',  # symbol
                ',': 'KC', # punctuation comma
                '-': 'KO', # punctuation other   
                '.': 'KE', # punctuation EOS
                '/': 'KO', # punctuation other
                ':': 'KE', # punctuation EOS
                ';': 'KC', # punctuation comma
                '<': 'M',  # symbol
                '=': 'M',  # symbol
                '>': 'M',  # symbol
                '?': 'KE', # punctuation EOS
                '@': 'M',  # symbol
                '[': 'M',  # symbol
                '\\': 'KO',# punctuation other 
                ']': 'M',  # symbol
                '^': 'KO', # punctuation other 
                '_': 'KO', # punctuation other 
                '`': 'KO', # punctuation other 
                '{': 'KO', # punctuation other 
                '|': 'KO', # punctuation other 
                '}': 'KO', # punctuation other 
                '~': 'KO', # punctuation other 
                '}': 'KO', # punctuation other 
                '«': 'KQ', # punctuation quotation 
                '»': 'KQ', # punctuation quotation  
                '´': 'KO', # punctuation other 
                '......': 'KO',
                '.....': 'KO',
                '....': 'KO',
                '...': 'KO',
                '..': 'KO',
                }

# general blanket revisions
# without 3rd person plural removed from verbs
single_revisions_alt = {
                'SFSDL': 'SFSDP',
                'SFPAL': 'SFPAP',
                'SFPDAL': 'SFPDAP',
                'SFPDL': 'SFPDP',
                'SFPGL': 'SFPGP',
                'SFPNL': 'SFPNP',
                'SFSAAL': 'SFSAAP',
                'SFSAL': 'SFSAP',
                'SFSDAL': 'SFSDAP',
                'SFSDL': 'SFSDP',
                'SFSGL': 'SFSGP',
                'SFSNAL': 'SFSNAP',
                'SFSNL': 'SFSNP',
                'SMPDL': 'SMPDP',
                'SMSAL': 'SMSAP',
                'SMSDAL': 'SMSDAP',
                'SMSDL': 'SMSDP',
                'SMSGL': 'SMSGP',
                'SMSNL': 'SMSNP',
                'SNPDL': 'SNPDP',
                'SNPNL': 'SNPNP',
                'SNSAAL': 'SNSAAP',
                'SNSAL': 'SNSAP',
                'SNSDAL': 'SNSDAP',
                'SNSDL': 'SNSDP',
                'SNSGL': 'SNSGP',
                'SNSNAL': 'SNSNAP',
                'SNSNL': 'SNSNP',
                'SXL': 'SXP',
                'DA': 'DG',
                'DD': 'DG',
                'DCA': 'DCG',
                'DCD': 'DCG',
                'DSA': 'DSG',
                'DSD': 'DSG',
                'EN': 'DN',
                'EA': 'DG',
                'ED': 'DG',
                'EG': 'DG',
                'I': 'DI',
                # VA tag converted to VANSN (as done in MIM GOLD)
                'VA': 'VANSN',
                # Person removed from plural verbs (skipped in alt dict)
                # 'VEAP1': 'VEAP',
                # 'VEAP3': 'VEAP',
                # 'VEPP1': 'VEPP',
                # 'VEPP2': 'VEPP',
                # 'VEPP3': 'VEPP',
                # 'VNAP1': 'VNAP',
                # 'VNAP3': 'VNAP',
                # 'VNPP1': 'VNPP',
                # 'VNPP2': 'VNPP',
                # 'VNPP3': 'VNPP',
                # 'T': 'DT', # NOT REMOVED
                '!': 'KE', # punctuation EOS
                '"': 'KQ', # punctuation quotation 
                '#': 'KO', # punctuation 
                '$': 'M',  # symbol
                '%': 'M',  # symbol
                '&': 'M',  # symbol
                "'": 'KQ',
                '(': 'KO', # punctuation other
                ')': 'KO', # punctuation other
                '*': 'KO', # punctuation other
                '+': 'M',  # symbol
                ',': 'KC', # punctuation comma
                '-': 'KO', # punctuation other   
                '.': 'KE', # punctuation EOS
                '/': 'KO', # punctuation other
                ':': 'KE', # punctuation EOS
                ';': 'KC', # punctuation comma
                '<': 'M',  # symbol
                '=': 'M',  # symbol
                '>': 'M',  # symbol
                '?': 'KE', # punctuation EOS
                '@': 'M',  # symbol
                '[': 'M',  # symbol
                '\\': 'KO',# punctuation other 
                ']': 'M',  # symbol
                '^': 'KO', # punctuation other 
                '_': 'KO', # punctuation other 
                '`': 'KO', # punctuation other 
                '{': 'KO', # punctuation other 
                '|': 'KO', # punctuation other 
                '}': 'KO', # punctuation other 
                '~': 'KO', # punctuation other 
                '}': 'KO', # punctuation other 
                '«': 'KQ', # punctuation quotation 
                '»': 'KQ', # punctuation quotation  
                '´': 'KO', # punctuation other 
                '......': 'KO',
                '.....': 'KO',
                '....': 'KO',
                '...': 'KO',
                '..': 'KO',
                }

single_errors = {
                'fýra\tNONPD': 'fýra\tNCNPD', 
                'tíggju\tNOMPD': 'tíggju\tNCMPD',
                'fyrstur\tNOMSN': 'fyrstur\tASSMSN',
                'næstur\tNOMSN': 'næstur\tASSMSN',
                'tveir\tNMPA': 'tveir\tNCMPA',
                'tveir\tNMSA': 'tveir\tNCMPA'
                 }

numerical_revisions = {}

# !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

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
    
def join_punctuation(corpus_list):
    for i in reversed(range(len(corpus_list))):
        # print(corpus_list[i])
        if len(corpus_list[i]):
            if corpus_list[i][0] in {'', '\n'}: continue
            elif corpus_list[i][1] == '.' and corpus_list[i-1][1] == '.' \
                and corpus_list[i-2][1] == '.' and corpus_list[i-3][1] == '.' \
                and corpus_list[i-4][1] == '.' and corpus_list[i-5][1] == '.':
                    corpus_list[i] = ['......', '......']
                    corpus_list[i-1] = corpus_list[i-2] = corpus_list[i-3] = \
                    corpus_list[i-4] = corpus_list[i-5] = []
            elif corpus_list[i][1] == '.' and corpus_list[i-1][1] == '.' \
                and corpus_list[i-2][1] == '.' and corpus_list[i-3][1] == '.' \
                and corpus_list[i-4][1] == '.':
                    corpus_list[i] = ['.....', '.....']
                    corpus_list[i-1] = corpus_list[i-2] = corpus_list[i-3] = \
                    corpus_list[i-3] = []
            elif corpus_list[i][1] == '.' and corpus_list[i-1][1] == '.' \
                and corpus_list[i-2][1] == '.' and corpus_list[i-3][1] == '.':
                    corpus_list[i] = ['....', '....']
                    corpus_list[i-1] = corpus_list[i-2] = corpus_list[i-3] = []
            elif corpus_list[i][1] == '.' and corpus_list[i-1][1] == '.' and corpus_list[i-2][1] == '.':
                corpus_list[i] = ['...', '...']
                corpus_list[i-1] = corpus_list[i-2] = []
            elif corpus_list[i][1] == '.' and corpus_list[i-1][1] == '.':
                corpus_list[i] = ['..', '..']
                corpus_list[i-1] = []
    return corpus_list

def clean_comments(corpus_list):
    cleaned = []
    sentence = []
    for token in corpus_list:
        if re.search(r'^%%', token[0]): continue
        elif re.search(r'\u00AD', token[0]): continue
        elif token[0].strip() == '':
            if len(sentence):
                sentence.append([''])
                cleaned.append(sentence)
                sentence = []
            else:
                continue
        else:
            sentence.append(token)
    # corpus_list = corpus_list[1:] if corpus_list[0] == [''] else corpus_list
    cleaned.append(sentence)
    return [token for sentence in cleaned for token in sentence]

def update_tags(corpus, verbal_person):
    
    # all revisions made gathered in list (for debugging)
    revised_lines = [] 
    
    # RegEx strings for pronouns (match specific tokens)
    PP_STRING = r'^((sjálv|tei(m|r)|(h[aoe]n+s?)|seg|(t|m|s)ær|hún|(t|s)ín?)(an|(i|a|u)(ri?|m)?|t|a?ra|s)?|t(ey|að|ess))$'
    PE_STRING = r'^(((t|m|s)ín?|vár|okk|henn|hans)((a|i|u)(r(a|i)|m)?|s|tt?)?)$'
    PI_STRING = r'^((sjálv|slík|tílík|s(a|o)m|summ)(an|(i|a|u)(ri?|m)?|t)?)$' # GREEDY
    # PI_STRING = r'^s[oa]m[iau]$' # Only catches forms of 'sama'
    PB_STRING = r'[øa]ll((a|i|um?)(n|r)?i?)?$'
    PQ_STRING = r'hv[aø](r(j(ar?|i|um)|t)?|nn?|t)$'
    
    for i in range(len(corpus)):
        # empty list declared for current revision
        revision = []
        revision.append(tuple(corpus[i])) # current line added to curr. revision
        
        if len(corpus[i]) < 2:
            continue
        try:
            if verbal_person:
                corpus[i][1] = single_revisions_alt[corpus[i][1]]
            else:
                corpus[i][1] = single_revisions[corpus[i][1]]
        except KeyError:
            
            # PRONOUNS
            if corpus[i][1][0] == 'P':
                # already differentiated pronoun tags (PI, PD)
                if len(corpus[i][1]) == 5:
                    # tags starting with PI converted to PB
                    if corpus[i][1].startswith('PI'):
                        corpus[i][1] = 'PB' + corpus[i][1][2:]
                    # no change made to PD tags
                    else: 
                        continue
                # short pronoun tags (to become PP, PE)
                else:
                    # tags with person become PP (P1PA -> PP1PA)
                    if corpus[i][1][1].isdigit():
                        corpus[i][1] = 'P' + corpus[i][1]
                    # matched tokens become PP
                    elif re.search(PP_STRING, corpus[i][0].lower()):
                        corpus[i][1] = corpus[i][1][:1] + 'P' + corpus[i][1][1:]
                    # other matched tokens become PE
                    elif re.search(PE_STRING, corpus[i][0].lower()):
                        corpus[i][1] = corpus[i][1][:1] + 'E' + corpus[i][1][1:]
                    # forms of 'allur' becomes PB
                    elif re.search(PB_STRING, corpus[i][0].lower()):
                        corpus[i][1] = corpus[i][1][:1] + 'B' + corpus[i][1][1:]
                    # forms of 'hver' ('hvat', etc.) not already PB, become PQ
                    elif re.search(PQ_STRING, corpus[i][0].lower()):
                        corpus[i][1] = corpus[i][1][:1] + 'Q' + corpus[i][1][1:]
                    # rest becomes PI
                    else:
                        corpus[i][1] = corpus[i][1][:1] + 'I' + corpus[i][1][1:]
                    
            # certain adjective tags to be converted to pronouns
            if corpus[i][1][0] == 'A':
                # NOTE: Some words (notably forms of 'sjálvur') should be 
                # differentiated to either PI or PP but are generalized as PI here
                if re.search(PI_STRING, corpus[i][0].lower()):
                    corpus[i][1] = 'PI' + corpus[i][1][3:]
                if re.search(PB_STRING, corpus[i][0].lower()):
                    corpus[i][1] = 'PB' + corpus[i][1][3:]
            
            
            # ABBREVATIONS
            if corpus[i][1] == 'T':
                if '.' not in corpus[i][0]:
                    corpus[i][1] = 'TS'
                elif re.search(r'.\..\.', corpus[i][0]):
                    corpus[i][1] = 'TS'
                else:
                    corpus[i][1] = 'TT'
            
            # NUMERALS
            if corpus[i][1][0] == 'N':
                if len(corpus[i+1]) < 2:
                    corpus[i][1] = 'NO'
                    continue
                # if next token is also numeral
                elif corpus[i+1][1][0] == 'N':
                    corpus[i][1] = 'NR'
                # checks next token if numeral is percentage
                elif re.search(r'(prosent|%)', corpus[i+1][0]):
                    corpus[i][1] = 'NP'
                # catches clocks, long numbers and years, tag as NO
                elif re.match(r'(\d\d?[.:]\d\d|\d\d\d\d|\d+[.,]\d+)$', corpus[i][0]):
                    corpus[i][1] = 'NO'
                # converts all digits to NO tag
                elif re.search(r'\d+', corpus[i][0]):
                    # checks for '.' in next token
                    if corpus[i+1][0] == '.':
                        # joins numeral if incorrectly tokenized
                        if re.match(r'\d+$', corpus[i+2][0]):
                            corpus[i][0] += '.' + corpus[i+2][0]
                            corpus[i+1] = corpus[i+2] = []
                        # joins punctutation to ordinal digit token (21., etc.)
                        else:
                            corpus[i][0] += '.'
                            corpus[i+1] = []
                    corpus[i][1] = 'NO'
                # fyrsti/fyrsta/fyrstu - tagged as superlative adjective
                elif re.match(fyrsti_token, corpus[i][0].lower()):
                    corpus[i][1] = numeral_revisions_superlative[corpus[i][1]]
                # other written ordinals - tagged as positive adjectives
                elif re.match(ordinal_token, corpus[i][0].lower()):
                    corpus[i][1] = numeral_revisions_positive[corpus[i][1]]
            
            # UNTAGGED (X)
            if corpus[i][1] == 'X':
                # web addresses (2 in corpus) get W tag
                if corpus[i][0].startswith('www.'):
                    corpus[i][1] = 'W'
            
        # after revisions, current line added to current revision
        revision.append(tuple(corpus[i])) 
        # if change made on tags, revision saved for debug log
        if revision[0][1] != revision[1][1]:
            revised_lines.append(tuple(revision))
    
    # output list for revisions declared
    revisions = []
    # all revised input lines sorted and duplicates removed
    for line in sorted(set(revised_lines)):
        revisions.append(f'{line[0][0]}\t{line[0][1]}\t{line[1][1]}')
        
    return corpus, revisions

def add_newlines(corpus):
    new_corpus = []
    for i in range(len(corpus)):
        # print(corpus[i])
        if i+1 < len(corpus):
            if corpus[i][0] in EOS_TOKENS \
            and corpus[i+1][0].strip() not in EOS_TOKENS:
                new_corpus.append(corpus[i])
                new_corpus.append([])
            else:
                new_corpus.append(corpus[i])
        else:
            new_corpus.append(corpus[i])
    # for i in range(len(corpus)):
    #     if corpus[i][0] in {'.', '?', '!', '...', '..'} and corpus[i+1][0] not in {'\n', ''}:
    #         if corpus[i+1][0][0].isupper():
    #             # print(corpus[i])
    #             # print(corpus[i+1])
    #             corpus[i+1][0] = '\n' + corpus[i+1][0]
    return new_corpus

def clean_question_marks(corpus):
    new_corpus = []
    for i in reversed(range(len(corpus))):
        if i+1 < len(corpus):
            if corpus[i] == []: 
                new_corpus.append([])
                # continue
            elif corpus[i][0] == '?' and corpus[i+1] == []:
                # new_corpus.append([])
                continue
            else:
                new_corpus.append(corpus[i])
        else:
            new_corpus.append(corpus[i])
    return reversed(new_corpus)

def clean_double_newlines(corpus):
    new_corpus = []
    for i in range(len(corpus)):
        if i+1 < len(corpus):
            if corpus[i] in [[''], []] and corpus[i+1] in [[''], []]: 
                continue
            else:
                new_corpus.append(corpus[i])
        else:
            new_corpus.append(corpus[i])
    return new_corpus

def sub_semicolon(corpus):
    new_corpus = []
    for pair in corpus:
        if pair == [';', ';']:
            new_corpus.append(['+', '+'])
        else:
            new_corpus.append(pair)
    return new_corpus

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help='path to input corpus file')
    parser.add_argument('--output', '-o', help='path to output (revised corpus file)')
    parser.add_argument('--clean_output', '-c', help='flag to clean comments etc. from input', action='store_true')
    parser.add_argument('--insert_newlines', '-n', help='flag to insert newlines after punctuation', action='store_true')
    parser.add_argument('--duplicates', '-d', help='flag to clear duplicate sentences from corpus', action='store_true')    
    parser.add_argument('--tags', '-t', help='flag to revise tags', action='store_true')
    parser.add_argument('--semicolon', '-s', help='flag to substitute ; with +', action='store_true')
    parser.add_argument('--verbal_person', '-v', help='flag to not change person in plural verb tags', action='store_true')
    args = parser.parse_args()
    
    corpus = get_corpus(args.input)

    if args.clean_output:
        corpus = clean_comments(corpus)
        corpus = join_punctuation(corpus)
        corpus = clean_question_marks(corpus)
        corpus = [i for i in corpus if i != []]
        
    if args.tags:
        corpus, revisions = update_tags(corpus, args.verbal_person)
        corpus = [i for i in corpus if i != []]
        with open(os.path.join(os.path.dirname(args.output), 'tag-revisions.txt'), 'w') as debug_info:
            for revision in revisions:
                debug_info.write(revision)
                debug_info.write('\n')
    
    if args.semicolon:
        corpus = sub_semicolon(corpus)
    
    if args.insert_newlines:
        corpus = add_newlines(corpus)
        
    corpus = clean_double_newlines(corpus)
    
    # # NOTE: not used
    # if args.duplicates:
    #     corps = clear_duplicates(corpus)
    
    with open(args.output, 'w') if args.output else stdout as output:
        for pair in corpus:
            line = '\t'.join(pair)+'\n'
            output.write(line)
        output.write('\n')
    
