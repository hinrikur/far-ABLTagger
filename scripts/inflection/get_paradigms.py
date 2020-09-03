
import os
import csv
import re
import sys

import argparse


# INFLECTIONS_PATH = sys.argv[1]


def main():

    parser = argparse.ArgumentParser(description='Access inflectional paradigms in Sigrúnarsnið formatted .csv file')
    parser.add_argument('--input', '-i', type=str, required=True, help='path to input .csv file')

    categories = parser.add_mutually_exclusive_group(required=True)
    categories.add_argument('--nouns', '-no', help='returns inflection data for nouns', action='store_true')
    categories.add_argument('--verbs', '-so', help='returns inflection data for verbs', action='store_true')
    categories.add_argument('--adjectives', '-lo', help='returns inflection data for adjectives', action='store_true')
    categories.add_argument('--numerals', '-to', help='returns inflection data for numerals', action='store_true')
    categories.add_argument('--other', '-o', help='returns inflection data for other word classes', action='store_true')
    categories.add_argument('--all', '-a', help='returns inflection data for all word classes', action='store_true')

    args = parser.parse_args()

    input_file_path = args.input
    with open(input_file_path) as f:
        infl_reader= csv.reader(f, delimiter=';')
        for row in infl_reader:
            if args.nouns:
                if row[2] in {'kk', 'kvk', 'hk',}:
                    print(row)
                else:
                    continue
            elif args.verbs:
                if row[2] == 'so':
                    print(row)
                else:
                    continue
            elif args.adjectives:
                if row[2] == 'lo':
                    print(row)
                else:
                    continue
            elif args.numerals:
                if row[2] == 'to':
                    print(row)
                else:
                    continue
            elif args.other:
                if row[2] not in {'kk', 'kvk', 'hk', 'so', 'lo', 'to'}:
                    print(row)
                else:
                    continue
            elif args.all:
                print(row)

if __name__ == '__main__':
    main()
