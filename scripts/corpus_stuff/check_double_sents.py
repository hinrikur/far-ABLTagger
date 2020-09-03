import argparse
from sys import stdout
from collections import Counter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help='path to input corpus file')
    parser.add_argument('--output', '-o', help='path to output (revised corpus file)')
    parser.add_argument('--fix', '-f', help='flag if write fixed sentences to file', action='store_true')
    args = parser.parse_args()

    corpus = [] 
    with open(args.input,'r') as file:
        sentence = []
        for line in file.readlines():
            if line.strip() == '' and len(sentence):
                corpus.append('\n'.join(sentence))
                sentence = []
            else:
                sentence.append(line.strip('\n'))
                
    print('No. of sents in corpus:',len(corpus))
    print('No. of individual sents:',len(set(corpus)))
            
    cnt = Counter()

    for s in corpus:
        cnt[s] +=1
        
    doubles = []

    for k,v in cnt.items():
        if v > 1 and len(k) > 3:
            doubles.append(k)

    out_corpus = []
    apparent_doubles = []
    for sent in corpus:
        if sent not in out_corpus:
            out_corpus.append(sent)
        else:
            apparent_doubles.append(sent)
            
    if args.fix:
        with open(args.output, 'w') if args.output else stdout as out:
            for sent in out_corpus:
                out.write(sent)
                out.write('\n\n')
                
    elif not args.fix:
        with open(args.output, 'w') if args.output else stdout as out:
            for sent in doubles:
                out.write(sent)
                out.write('\n\n')
