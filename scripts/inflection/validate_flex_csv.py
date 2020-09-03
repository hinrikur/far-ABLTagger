import sys
import csv
import argparse
from collections import defaultdict



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', metavar='FILE_PATH', help='path to input csv file')
    parser.add_argument('--index', help='index of word to print', default=None)
    parser.add_argument('--lemma', help='lemma of word to print', default=None)
    parser.add_argument('--stats', action='store_true', help='flag if getting word class stats from csv')
    args = parser.parse_args()


    # classes = defaultdict(int)
    class_indexes = defaultdict(set)

    filename = args.input_file
    index = args.index

    with open(filename, newline='') as csvfile:
        flexreader = csv.reader(csvfile, delimiter=';')
        for row in flexreader:
            if args.index:
                # print(row[1], index)
                if row[1] == index:
                    print(row)
                # elif int(row[1])>int(index):
                #     exit()
            elif args.stats:
                class_indexes[row[2]].add(row[1])
            elif args.lemma:
                if row[0] == args.lemma:
                    print(row)
    if args.stats:
        print('Words per word class:')
        for k,v in class_indexes.items():
            print(f'{k}\t{len(v)}')
        # print('Lines per word class:')
        # for k,v in classes.items():
        #     print(f'{k}\t{v}')

if __name__ == '__main__':
    main()
