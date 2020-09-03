import re

def clean_category(cat):
    class_regex = r'(kv-n|k-n|kv|k|l|hj|h|lh|fs|sb|mðlv|s|sern|fn|ljóðh|kve|t|hvmf|n|flt|miðst|hást|kób|f|við|hvnf|boðsh|hób|hvsf|ób|kn)'
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

list1 = ['h/k', 'h/kv', 'h:', 'hj:', 'hk', 'hób',]

for i in list1:
    print(i, clean_category(i))
    
