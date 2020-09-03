import sys
import os
import json
import argparse

"""
Script for extracting generated Sigrúnarsnið information from json files and 
save them in specific text files.
"""

# usage:
# python3 scripts/inflection/SH_from_json.py -i FO_inflection_data/sprotin/json-SH/* -o FO_inflection_data/SH_snid_output/

def get_json(file):
    sprotin_file = open(file, 'r')
    json_file = json.load(sprotin_file)
    return json_file

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', help='path to output FOLDER')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--input', '-i', nargs='+', required=True, 
                               default=argparse.SUPPRESS, help='')
    args = parser.parse_args()
    
    for file_path in args.input:
        
        # other files / dirs filtered out
        if not file_path.endswith('.json'):
            continue
        
        # paths created
        JSON_PATH = file_path
        FILE_NAME = 'sprotin_' + os.path.basename(JSON_PATH).replace('.json', '.txt')
        output_file = os.path.join(args.output, FILE_NAME) if args.output else None
        
        # JSON data read from file
        data = get_json(JSON_PATH)
        
        with open(output_file, 'w') if output_file else sys.stdout as out:
            for word in data['words']:
                sh = word.get('SH')
                if not sh: continue
                for word_form in sh:
                    out.write(';'.join([str(i) for i in word_form]))
                    out.write('\n')
                out.write('\n')
        
        # file deleted if empty
        if args.output:
            if os.stat(output_file).st_size == 0:
                os.remove(output_file)
