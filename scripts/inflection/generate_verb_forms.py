
import re
import csv
import sys
import os
from collections import defaultdict
# from stemtest import *

ABLAUT_CLASSES = ['14', '15', '16', '17', '18', '19', '20', '22', '23', 
                  '24', '31', '32', '33', '34', '35', '36', '37', '38', '39', 
                  '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', 
                  '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', 
                  '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', 
                  '72', '80', '91', '98',
                  '15_2']

MIDDLE_CLASSES = ['1_m', '2_m', '3_m', '4_m', '5_m', '6_m', '7_m', '8_m', '9_m',
                  '10_m', '11_m', '12_m', '13_m', '14_m', '15_m', '15_2_m']

VERB_SUFFIX = r'(a|að|aðu|ar|i|u|in|st|ð|ði|ðu|ggja|ður|aður|di|du|dur|dist|dust|ddist|ddust|ddur|ddi|ddu|ir|ið|andi|ast|jast|ist|j|ji|jir|jið|ja|jandi|ur|tu|ti|tur|tist|tust|tast|t|tt|)$'
PREFIX = r'^(aftrat|undir|uppi|upp|at|av|desi|eftir|fyri|fíggjar|gjøgnum|hjá|hóast|innan|løg|lýð|millum|mis|móti|pá|sam|sambært|senti|smá|summum|síðan|til|tor|um|umframt|undan|uttan|ver|við|viðvíkjandi|yvir|á|í|íggj|ígjøgnum|ímillum|ímóti|ó|úr|ser)'

def write_tsv(fh, l):
    with open(fh+'.tsv', 'w') as f:
        for i in l:
            f.write('\t'.join(i))
            f.write('\n')

def get_paradigms(fh, type):
    if type == 'list':
        paradigms = []
    elif type == 'dict':
        paradigms = {}
    with open(fh, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        # next(reader)
        for row in reader:
            if row[1] == '': continue
            if type == 'list':
                paradigms.append(row)
            elif type == 'dict':
                paradigms[row[0]] = row[1:]
            
    return paradigms

def fix_single_errors(form):
    form = re.sub(r'staðandi$', 'standi', form)
    form = re.sub(r'bi$', 'bið', form)
    form = re.sub(r'lødu$', 'løgdu', form)
    form = re.sub(r'ladur$', 'lagdur', form)
    form = re.sub(r'lat$', 'lagt', form)
    # orm = re.sub(r'bruttu$', 'brutu', form) # bruttu - brutu
    return form

def clean_output(form):
    # print(form)
    form = re.sub(r'(ðdd|ðjdd)', 'dd', form)
    form = re.sub(r'(ðtt|ðjtt)', 'tt', form)
    form = re.sub(r'ndd', 'nd', form)
    form = re.sub(r'ndt', 'nt', form)
    form = re.sub(r'rðd', 'rd', form)
    form = re.sub(r'rðt', 'rt', form)
    form = re.sub(r'stt', 'st', form)
    form = re.sub(r'nnd', 'nd', form)
    form = re.sub(r'nnt', 'nt', form)
    form = re.sub(r'ppt', 'pt', form)
    form = re.sub(r'kkt', 'kt', form)
    form = re.sub(r'kkd', 'kd', form)
    form = re.sub(r'ggd', 'gd', form)
    form = re.sub(r'ggð', 'gð', form)
    form = re.sub(r'ggt', 'gt', form)
    form = re.sub(r'sst', 'st', form) # geysst - geyst
    form = re.sub(r'ðð', 'ð', form)
    form = re.sub(r'ii', 'i', form)
    form = re.sub(r'ldt$', 'lt', form) # haldt - halt
    form = re.sub(r'tlð', 'tlað', form) # ætlði - ætlaði
    form = re.sub(r'ttt$', 'tt', form) # fluttt - flutt
    form = re.sub(r'nnst', 'nst', form) # brannst - branst
    form = re.sub(r'kkst', 'kst', form) # stakkst - stakst
    form = re.sub(r'rr$', 'r', form) # goyrr - goyr
    form = re.sub(r'rrt', 'rt', form) # goyrrt - goyrt
    form = re.sub(r'ittu$', 'itu', form) # bittu - bítu
    form = re.sub(r'ýttur$', 'ýtur', form) # brýttur - brýtur
    form = re.sub(r'uttu$', 'utu', form) # bruttu - brutu
    form = re.sub(r'eitt$', 'eit', form) # beitt - beit
    form = re.sub(r'eitt/', 'eit/', form) # beitt/beitst - beit/beitst
    form = re.sub(r'eytt$', 'eyt', form) # beitt - beit
    form = re.sub(r'eytt/', 'eyt/', form) # beitt/beitst - beit/beitst
    form = re.sub(r'eei', 'ei', form) # framleeingjandi - framleingjandi
    form = re.sub(r'eo', 'e', form) # húðfleongjandi - húðflongjandi
    
    # form = re.sub(r'gj', 'nt', form)
    # form = re.sub(r'ppt', 'pt', form)


    # print(form)
    return fix_single_errors(form)

def get_suffix(form, form_stem, stem):
    if len(form)-len(re.search(VERB_SUFFIX, form)[0]) == 1 and form[0] not in 'aáiíyýuúeoóøæ':
        suffix = ''
    else:
        if re.search(stem, form):
            # print(1)
            suffix = re.sub(stem, '', form, 1)
        elif not re.search(form_stem, stem):
            # print(2)
            stem = form_stem
            suffix = re.sub(stem, '', form, 1)
        else:
            # print(3)
            suffix = re.search(VERB_SUFFIX, form)[0]
    return suffix

def get_info(form, display_word):
    stem = re.sub(r'(((gg)?j)?a$|j?a?st$)', '', display_word, 1)
    form_stem = re.sub(VERB_SUFFIX, '', form)
    stem_vowel = re.search(r'((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])', re.sub(VERB_SUFFIX, '', paradigm[1]))[0]
    form_stem_vowel = re.search(r'j?((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])(gv|ggj)?', form)[0]
    form_syll = re.sub(f'^[^({form_stem_vowel})]+', '', form)
    # stem_pref = re.search(f'^[^({form_stem_vowel})]+', form)
    return stem, form_stem, stem_vowel, form_stem_vowel, form_syll

def generate_new_form(form, vowel_suffix, ablaut=False):
        if vowel_suffix in {'', '-'}:
            return '-'
        else:
            if '/' in vowel_suffix or '/' in form:
                forms = form.split('/') if '/' in form else [form, form]
                vowels_suffixes = vowel_suffix.split('/') if '/' in vowel_suffix else [vowel_suffix, vowel_suffix]
                outputs = []
                # print(forms)
                # print(vowels_suffixes)
                for pair in zip(forms, vowels_suffixes):
                    # print(pair)
                    form = pair[0]
                    form_stem_vowel, suffix = pair[1].split(';')
                    form_stem = re.sub(r'(((gg)?j)?a$|j?a?st$)', '', form, 1)
                    output = form_stem+suffix
                    if ablaut:
                        vowels = re.findall(r'j?((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])(gv|ggj)?(?!ndi)', output)
                        if len(vowels) > 2:
                            # print(vowels)
                            # prefix, stem = output[:len(output)//2-1], output[len(output)//2-1:]
                            # TESTING NEW PREFIX STEM THING
                            prefix, stem = re.match(PREFIX, output)[0] if re.match(PREFIX, output) else '', re.sub(PREFIX, '', output)
                            stem = re.sub(r'j?((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])(gv|ggj)?(?!ndi|$)',  form_stem_vowel, stem, 1)
                            output = prefix+stem
                        else:
                            output = re.sub(r'j?((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])(gv|ggj)?(?!ndi|$)',  form_stem_vowel, output, 1)
                    # output = re.sub(r'(jgg|vg)?([aáiíyýuúeoóøæ]|([yi]e|yø|[iy]o|ua))j?',  form_stem_vowel[::-1], output[::-1], 1)[::-1]
                    outputs.append(clean_output(output))
                output = '/'.join(outputs)
                # return 'TODO'
            else:
                # print(form, vowel_suffix)
                # stem, form_stem, stem_vowel, form_stem_vowel, form_syll = get_info(form, display_word)
                form_stem_vowel, suffix = vowel_suffix.split(';')
                form_stem = re.sub(r'(((gg)?j)?a$|j?a?st$)', '', form, 1)
                output = form_stem+suffix
                if ablaut:
                    vowels = re.findall(r'j?((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])(gv|ggj)?(?!ndi)', output)
                    if len(vowels) > 2:
                        # print(vowels)
                        # prefix, stem = output[:len(output)//2], output[len(output)//2:]
                        # TESTING NEW PREFIX STEM THING
                        prefix, stem = re.match(PREFIX, output)[0] if re.match(PREFIX, output) else '', re.sub(PREFIX, '', output)
                        stem = re.sub(r'j?((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])(gv|ggj)?(?!ndi|$)',  form_stem_vowel, stem, 1)
                        output = prefix+stem
                    else:
                        output = re.sub(r'j?((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])(gv|ggj)?(?!ndi|$)',  form_stem_vowel, output, 1)
                    # output = re.sub(r'(jgg|vg)?([aáiíyýuúeoóøæ]|([yi]e|yø|[iy]o|ua))j?',  form_stem_vowel[::-1], output[::-1], 1)[::-1]
                    output = clean_output(output)
                else:
                    output = clean_output(output)
        return output


def generate_output(form, display_word):
    if form in {'', '-'}:
        return '-', '-'
    else:
        if '/' in display_word or '/' in form:
            stems, forms = display_word.split('/'), form.split('/')
            if len(stems) == 1:
                stems = stems + stems
            out_stems, out_vowels, out_suffixes, out_syls, outputs = [], [], [], [], []
            for pair in zip(forms, stems):
                # print(pair)
                stem, form_stem, stem_vowel, form_stem_vowel, form_syll = get_info(pair[0], pair[1])
                suffix = get_suffix(pair[0], form_stem, stem)
                out_stems.append(stem)
                out_vowels.append(form_stem_vowel)
                outputs.append(clean_output(stem+suffix, form_stem_vowel))
                out_suffixes.append(suffix)
            # stem_suf = '/'.join([';'.join(list(i)) for i in zip(out_stems, out_suffixes)])
            stem_vow = '/'.join([';'.join(list(i)) for i in zip(out_vowels, out_suffixes)])
            # print(stem_suf)
            output = stem_vow, '/'.join(outputs)
            # print(output)
            return output
        else:
            stem, form_stem, stem_vowel, form_stem_vowel, form_syll = get_info(form, display_word)
            suffix = get_suffix(form, form_stem, stem)
            output = form_stem_vowel+';'+suffix, clean_output(stem+suffix, form_stem_vowel)
    return output


def get_lemmas(fh):
    lemmas = defaultdict(list)
    # with open(f'FO_inflection_data/uninflected/{fh}.tsv') as f:
    with open(fh) as f:
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            lemmas[line[0]].append(line[1:])
    return lemmas

def merge_forms(list1, list2):
    out_list = []
    for i in range(len(list2)):
        if list1[i] == '':
            out_list.append(list2[i])
        elif '/' in list2[i] and not '/' in list1[i]:
            out_list.append(list2[i])
        else:
            out_list.append(list1[i])
        # out_list.append(list1[i]) if list1[i] != '' else out_list.append(list2[i])
    return out_list

def generate_new_paradigms(p_list, l_dict):
    output_paradigms = []
    for paradigm in p_list:
        p_class = paradigm[0]
        p_class_num = re.sub('_m', '', p_class)
        lemma_list = l_dict[p_class_num]
        if p_class_num in ABLAUT_CLASSES:
            print(p_class, 'ABLAUT')
        else:
            # continue
            print(p_class)
        
        suffixes = paradigm[1:]
        for forms in lemma_list:
            lemma = forms[0]
            
            # Available forms extracted if not middle voice class 
            if p_class.endswith('_m') or len(forms) == 1:
                available_forms = ['',       '', '',    '',       '', '',       '',   '',  '',        '', '',  '',    '',       '',       '']
            else:
                #                  nh        1nt 2nt    3nt       ft. 1þt       2þt   3þt   ft.       bh  bhft lh1    lh2       lh.tát	hugsh.
                available_forms = [forms[1], '', '',    forms[2], '', forms[3], '',   '',   forms[4], '', '',  '',    forms[6], forms[5], '']
                #                  rykkja    x   x      rykkir    x   rykti     x     x     ryktu     x   x    x      ryktur    x         x
                #                  e;a       e;i e;/e;t e;        e;a jø;di     jø;di jø;di jø;du     e;  e;ið e;andi jø;dur    jø;t      e;i
            
            # New forms generated
            new_forms = []
            for vowel_suffix in suffixes:
                if p_class_num in ABLAUT_CLASSES:
                        new_form = generate_new_form(lemma, vowel_suffix, ablaut=True)
                else:
                    new_form = generate_new_form(lemma, vowel_suffix)
                new_forms.append(new_form)
            output_forms = merge_forms(available_forms, new_forms)
            
            # print(available_forms)
            # print(new_forms)
            # print(output_forms)]
            # print([p_class].extend(output_forms))
            
            # # DEBUG:
            # names = ['nh', '1nt', '2nt',    '3nt',       'ft', '1þt',     '2þt',   '3þt',   'ft',      'bh',  'bhft', 'lh1',    'lh2',       'lhþt', 'hugsh']
            # for i in zip(names, output_forms, new_forms,  available_forms,):
            #     print('\t'.join(i))
            # input()
            output_paradigms.append([p_class] + output_forms)
    return output_paradigms

def generate_paradigms_json(paradigm_dict, json_object):
    p_classes = re.findall(r'\d+', ''.join(json_object['InflexCats']))
    # print(p_classes)
    if not p_classes:
        print('No inflection category for verb:', json_object['DisplayWord'])
        return
    # for p_class in p_classes:
    # NOTE: only first class picked
    p_class = p_classes[0]
    p_class_num = re.sub('_m', '', p_class) # this should not be needed but kept in case
    middle_class = p_class_num + '_m'
    suffixes = paradigm_dict[p_class]
    
    # print(json_object['InflectedForm'])
    forms = json_object['InflectedForm']
    if not forms:
        print('No inflection forms for verb:', json_object['DisplayWord'])
        return
    # print(forms)
    lemma = forms[0] if forms else None
    
    # # TEMP: added check for Middle voice in lemma, returns none if so
    # if lemma[-2:] == 'st':
    #     return None
    
    # Available forms extracted if not middle voice class 
    # Note: no middle classes in Sprotin json data
    if p_class.endswith('_m') or len(forms) == 1:
        available_forms = ['',       '', '',    '',       '', '',       '',   '',  '',        '', '',  '',    '',       '',       '']
    else:
        #                  nh        1nt 2nt    3nt       ft. 1þt       2þt   3þt   ft.       bh  bhft lh1    lh2       lh.tát	hugsh.
        available_forms = [forms[0], '', '',    forms[1], '', forms[2], '',   '',   forms[3], '', '',  '',    forms[5], forms[4], '']
        #                  rykkja    x   x      rykkir    x   rykti     x     x     ryktu     x   x    x      ryktur    x         x
        #                  e;a       e;i e;/e;t e;        e;a jø;di     jø;di jø;di jø;du     e;  e;ið e;andi jø;dur    jø;t      e;i
        
    # New forms generated
    new_forms = []
    for vowel_suffix in suffixes:
        if p_class_num in ABLAUT_CLASSES:
            new_form = generate_new_form(lemma, vowel_suffix, ablaut=True)
        else:
            new_form = generate_new_form(lemma, vowel_suffix)
        new_forms.append(new_form)
    output_forms = merge_forms(available_forms, new_forms)
    
    # Middle voice forms generated if applicable
    if p_class_num + '_m' in MIDDLE_CLASSES:
        middle_forms = []
        middle_suffixes = paradigm_dict[middle_class]
        for vowel_suffix in middle_suffixes:
            if p_class_num in ABLAUT_CLASSES:
                new_form = generate_new_form(lemma, vowel_suffix, ablaut=True)
            else:
                new_form = generate_new_form(lemma, vowel_suffix)
            middle_forms.append(new_form)
        output_forms = output_forms + middle_forms
    return output_forms


def main():
    
    TSV_FILE_NAME = sys.argv[1] # e.g. 's' for verbs
    # OUT_FILE_NAME = TSV_FILE_NAME + '_paradigms'
    OUT_FILE_NAME = os.path.join('FO_inflection_data/generated_paradigms/inflected', \
                                 os.path.splitext(os.path.basename(TSV_FILE_NAME))[0]\
                                 + '_inflected')

    paradigm_list = get_paradigms('FO_inflection_data/hj/verb_suffixes.tsv', 'list')
    paradigm_dict = get_paradigms('FO_inflection_data/hj/verb_suffixes.tsv', 'dict')

    lemmas = get_lemmas(TSV_FILE_NAME)
        
    paradigms = generate_new_paradigms(paradigm_list, lemmas)
    
    write_tsv(OUT_FILE_NAME, paradigms)
        
if __name__ == '__main__':

    main()
    

# 14 ei o	ei	o	ei	o	ei	o	ei	o	o	o	o	o	o	ei	o	ei	o	o	o	ei	o
# 14_m ei o	ei	o	ei	o	ei	o	ei	o	o	o	o	o	-	-	-	-	-	ei	o
# 15 ei o	ei	o	ei	o	ei	o	ei	o	o	o	o	o	o	ei	o	ei	o	o	o	ei	o
# 15_m ei o	ei	o	ei	o	ei	o	ei	o	o	o	o	o	-	-	-	-	-	ei	o
# 15_2 ei ei	ei	ei	ei	o	o	o	o	ei	ei	ei	o	o	ei
# 16 e e	e	e	e	a	a	a	a	e	e	e	a	a	e
# 17 e e	e	e	e	a	a	a	a	e	e	e	a	a	e
# 18 e e	e	e	e	a	a	a	a	e	e	e	a	a	e
# 19 y y	y	y	y	u	u	u	u	y	y	y	u	u	y
# 20 eggj e	e	e	eggj	e	e	e	ø	e	e	eggj	a	a	e
# 22 y y	y	y	y	u	u	u	u	y	y	y	u	u	y
# 22_1 ý ý	ý	ý	ý	ý	ý	u	ý	u	ý	u	ý	u	ý	ý	ý	ý	u	ý	u	ý	ý
# 23 y y	y	y	y	y	u	u	u	u	y	y	y	u	u	y
# 24 y y	y	y	y	u	u	u	u	y	y	y	u	u	y
# 31 e e	e	e	e	e	jø	jø	jø	jø	e	e	e	jø	jø	e
# 32 úgv úgv	ý	ý	ý	úgv	ú	ú	ú	ú	úgv	úgv	úgv	úgv	ú	úgv
# 33 ógv ógv	ø	ø	ø	ógv	ó	ó	ó	ó	ógv	ógv	ógv	ógv	ó	ógv
# 35 í í	í	í	í	ei	ei	ei	ei	i	í	í	í	i	i	í
# 36 í í	í	í	í	ei	ei	ei	ei	i	í	í	í	i	i	í
# 37 ó ó	ý	ý	ó	ey	ey	ey	ey	u	ó	ó	ó	o	o	ó
# 38 jó jó	jý	jý	jó	ey	ey	ey	ey	u	jó	jó	jó	o	o	jó
# 39 jó jó	ý	ý	jó	ey	ey	ey	ey	u	jó	jó	jó	jó	o	o	jó
# 39d jó jó	ý	ý	jó	ey	ey	ey	ey	u	jó	jó	jó	jó	o	o	jó
# 39s jó jó	ý	ý	jó	ey	ey	ey	ey	u	jó	jó	jó	jó	o	o	jó
# 40 ú ú	ý	ý	ú	ey	ey	ey	ey	u	ú	ú	ú	o	o	ú
# 41 úgv úgv	ý	ý	úgv	ey	ey	ey	ey	u	úgv	úgv	úgv	o	o	úgv
# 42 úgv úgv	ý	ý	úgv	ey	ey	ey	ey	u	úgv	úgv	úgv	o	o	úgv
# 44 i i	i	i	i	a	a	a	a	u	i	i	i	u	u	i
# 45 i i	i	i	i	a	a	a	a	u	i	i	i	u	u	i
# 46 i i	i	i	i	a	a	a	a	u	i	i	i	i	i	u	u	i
# 47 i i	i	i	i	a	a	a	a	u	i	i	i	o	o	i
# 48 e e	e	e	e	a	a	a	a	u	e	e	e	u	u	e
# 49 e e	e	e	e	a	a	a	a	u	e	e	e	o	o	e
# 50 ø ø	ø	ø	ø	a	ø	a	a	a	ø	u	ø	ø	ø	o	o	ø
# 51 a a	o	o	a	e	e	e	e	i	a	a	a	a	i	i	a
# 52 e e	e	e	e	a	a	a	a	ó	e	e	e	o	o	e
# 53 ey ey	oy	oy	ey	ey	ey	ey	ey	u	ey	ey	ey	o	o	ey
# 54 e e	e	e	e	e	a	a	a	a	ó	e	e	e	o	o	e
# 55 a a	e	e	e	a	ó	ó	ó	ó	ó	a	a	a	a	a	a
# 56 e e	e	e	e	a	a	a	a	ó	e	e	e	i	i	e
# 57 i i	i	i	i	a	a	a	a	ó	i	i	i	i	i	i
# 58 a a	e	e	a	ó	ó	ó	ó	ó	a	a	a	a	a	a
# 59 ja ja	je	je	ja	jó	jó	jó	jó	jó	ja	ja	ja	jo	o	jo	o	ja
# 60 a a	e	e	a	ó	ó	ó	ó	ó	a	a	a	i	i	a
# 61 a a	e	e	a	e	e	e	i	a	a	a	i	i	a
# 62 o o	e	e	o	a	a	a	a	ó	o	o	o	o	o	o
# 63 o o	e	e	o	o	o	o	o	o	o	o	o	o	o	o
# 64 a a	e	e	a	æ	æ	æ	æ	ó	a	a	a	a	a	a
# 64_1 á á	e	e	á	æ	æ	æ	æ	ó	á	á	á	á	á	á
# 65 a a	e	e	a	ó	ó	ó	ó	ó	a	a	a	a	a	a	a
# 66 i i	i	i	i	a	a	a	a	ó	i	i	i	i	i	i
# 67 a a	e	e	a	ó	ó	ó	ó	ó	a	a	a	i	i	a
# 68 ø ø	ø	ø	ø	a	a	a	a	u	ø	ø	ø	o	o	o	o	ø
# 69 á á	æ	æ	æ	á	ó	e	ó	ó	ó	e	ó	e	á	á	á	i	i	á
# 70 i i	i	i	i	e	e	e	ø	i	i	i	a	a	i
# 72 e e	e	e	e	á	á	á	á	ó	e	e	e	e	e	e
# 80 í í	í	í	í	í	í	ei	ei	ei	i	í	í	-	-	i	í
# 91 yggj y	y	y	yggj	u	u	u	u	y	y	yggj	u	u	y
# 98 íggj í	íggj	íggj	íggj	íggj	íggj	íggj	íggj	-	í	-	-	íggj	í
