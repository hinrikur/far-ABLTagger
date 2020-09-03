import wiktextract
import json
import sys
import os

path = r'utils/enwiktionary-20200620-pages-articles-multistream.xml.bz2'
out_path = r'FO_inflection_data/wiktionary'

if not os.path.isdir(out_path):
    os.mkdir(out_path)

cnt = []

def word_cb(data):
    cnt.append('')
    filename = str(data.get('pos', 'no-pos')) + '.json'
    out_file = os.path.join(out_path, filename)
    print(f'{len(cnt)}\t{data}')
    # json.dump(data, sys.stdout,  ensure_ascii=False, indent=4)
    with open(out_file, 'a') as output:
        json.dump(data, output,  ensure_ascii=False, indent=4)
        output.write('\n')
    
ctx = wiktextract.parse_wiktionary(
    path, word_cb,
    capture_cb=None,
    languages=["Faroese"],
    translations=False,
    pronunciations=False,
    redirects=False)
