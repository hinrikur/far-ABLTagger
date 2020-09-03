import os
import sys
from collections import defaultdict
import nefnir
import random

IN_FILE = '../corpora/OTB/OTB.txt'
WORD_OCCURANCE = sys.argv[1]
OUT_NUM = int(sys.argv[2])

nouns = defaultdict(int)

with open(IN_FILE) as otb:
    for line in otb.readlines():
        line = line.split('\t')
        if len(line) < 2:
            continue
        elif '-' in line[0] or '.' in line[0] :
            continue
        elif line[0][0].isupper():
            continue
        elif len(line[0]) == 1 and line[0] != 'á':
            continue
        elif line[1].strip()[0] in  {'n', 'l'}:
            lemma = nefnir.lemmatize(line[0], line[1].strip())
            nouns[lemma]+=1

# for key, value in sorted(nouns.items(), key=lambda item: item[1]):
#     print("%s: %s" % (key, value))

common = []
for k, v in nouns.items():
    if v > int(WORD_OCCURANCE):
        common.append(k)

# for n in random.sample(common, OUT_NUM):
#     print(n)


print(','.join(random.sample(common, OUT_NUM)))

# f = open(f'algeng_nafnord_{WORD_OCCURANCE}.txt', 'w')

# for n in sorted(common):
#     f.write(n)
#     f.write('\n')
#
# f.close()
