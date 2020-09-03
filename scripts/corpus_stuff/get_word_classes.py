
import sys
from collections import Counter


cnt = Counter()
with open(sys.argv[1]) as file:
    for line in file.readlines():
        line = line.split('\t')
        if len(line) == 1: continue
        w_class = line[1][0]
        cnt[w_class]+=1

for i in reversed(sorted(cnt)):
    print(i)
    
