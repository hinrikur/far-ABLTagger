import re
from stemtest import get_paradigms, clean_output

VERB_SUFFIX = r'(a|að|aðu|ar|i|u|in|st|ð|ði|ðu|ggja|ður|aður|di|du|dur|dist|dust|ddist|ddust|ddur|ddi|ddu|ir|ið|andi|ast|jast|ist|j|ji|jir|jið|ja|jandi|ur|tu|ti|tur|tist|tust|tast|t|tt|)$'

def write_tsv(fh, l):
    with open(fh+'.tsv', 'w') as f:
        for i in l:
            f.write('\t'.join(i))
            f.write('\n')


def main():
    paradigms = get_paradigms('verb_transpose.tsv')

    suffix_list = []
    for paradigm in paradigms:
        paradigm_suffixes = []
        p_class = paradigm[0]
        paradigm_suffixes.append(p_class)
        if re.match(r'([A-ZYÝIÍAÁOÓUÚÆØ]+|[a-zyýiíaáoóuúæø]+)', p_class):
            continue
        # print('CLASS:', paradigm[0])
        stem = re.sub(r'(((gg)?j)?a$|j?a?st$)', '', paradigm[1], 1)
        if '/' in stem:
            stem = stem.split('/')[1]
        for form in paradigm[1:]:
            if form == '':
                paradigm_suffixes.append('')
            elif form == '-':
                paradigm_suffixes.append('-')
            else:
                if '/' in form:
                    form = form.split('/')[1]

                form_stem = re.sub(VERB_SUFFIX, '', form)

                stem_vowel = re.search(r'((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])', re.sub(VERB_SUFFIX, '', paradigm[1]))[0]
                form_stem_vowel = re.search(r'j?((e[iy]|øy|o[iy]|au)|[aáiíyýuúeoóøæ])(gv|ggj)?', form)[0]

                stem_vowel = None
                if len(form)-len(re.search(VERB_SUFFIX, form)[0]) == 1 and form[0] not in 'aáiíyýuúeoóøæ':
                    suffix = ''
                else:
                    if re.search(stem, form):
                        suffix = re.sub(stem, '', form)
                    elif not re.search(form_stem, stem):
                        stem = form_stem
                        suffix = re.sub(stem, '', form)
                    else:
                        suffix = re.search(VERB_SUFFIX, form)[0]

                try:
                    assert form == clean_output(stem+suffix, form_stem_vowel)
                    paradigm_suffixes.append(stem+';'+suffix)
                except:
                    raise
                    print(f'{form}\t{stem} {suffix} {clean_output(stem+suffix, form_stem_vowel)}\tERROR <'+'-'*20)
        # print('\t'.join(paradigm_suffixes))
        suffix_list.append(paradigm_suffixes)

    write_tsv('../FO_inflection_data/hj/verb_suffixes', suffix_list)

if __name__ == '__main__':
    main()
