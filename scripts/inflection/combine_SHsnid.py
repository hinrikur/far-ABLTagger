import os
import argparse
import sys
import shutil

# usage:
# python3 scripts/inflection/combine_SHsnid.py FO_inflection_data/SH_snid_output/ FO_inflection_data/SH_snid_output/COMBINED_TEST.csv

SPROTIN_WORD_CLASSES = ['h',  'hj', 'k-n', 'kob', 'kv',  'lh', 'hast', 'hob', 'k',  'kv-n', 'l',  's',  'k/h', 'kv/h', 'hj/mðlv', 'hj/l' 'hj:', 'h:' 'h/k', 'mðlv']
BIN_WORD_CLASSES =     ['hk', 'ao', 'kk',  'kk',  'kvk', 'lo', 'hk',   'hk',  'kk', 'kvk',  'lo', 'so', 'hk',  'hk',   'ao',      'ao',  'ao',  'hk', 'kk', 'uh']
WCLASS_DICT = dict(zip(SPROTIN_WORD_CLASSES, BIN_WORD_CLASSES))
# print(WCLASS_DICT)

def get_all_SHsnid_words(folder_handle):
    all_words = []
    filenames_to_skip = ['COMBINED_TEST.csv']
    word_classes_to_skip = [] # since there are errors in verbs, this should contain 's'
    for filename in os.listdir(folder_handle):
        if filename in filenames_to_skip: continue
        print(filename)
        file_class = os.path.splitext(filename)[0]
        if file_class in word_classes_to_skip: continue
        filepath = os.path.join(folder_handle, filename)
        with open(filepath, 'r') as file:
            lines = file.readlines()
            word_forms = []
            for line in lines:
                # if '-' in line: continue
                if line == '\n':
                    all_words.append(word_forms)
                    word_forms = []
                else:
                    line = line.strip('\n').split(';')
                    if line[1].isdigit():
                        line[1] = int(line[1])
                    word_forms.append(line)
    return all_words

def rename_classes(SH_list):
    # renamed_list = []
    for word in SH_list:
        for word_form in word:
            word_form[2] = WCLASS_DICT.get(word_form[2], word_form[2])
    # renamed_list.append(word)
    return SH_list


def enumerate_and_rename_words(SH_list, num_set):
    
    # list of words with no ID
    no_ID = []
    
    # counter for new IDs
    word_counter = 1
    # list of new IDs and old ones
    old_and_new_IDs = num_set
    
    for word in SH_list:
        # counter incremented until next free number found
        while word_counter in old_and_new_IDs:
            word_counter += 1
        # if no ID, new ID assigned
        if word[0][1] not in num_set:
            no_ID.append(word[0][0])
            for word_form in word:
                word_form[1] = word_counter
            old_and_new_IDs.add(word_counter)
            
        
    print('No. of words missing IDs:', len(no_ID)) 
    return SH_list
                    
def get_stats_and_ID_set(SH_list):
    combined_SH_snid = None
    
    sprotin_nums = []
    for word in SH_list:
        # print(word[0])
        if word[0][1] is not '':
            sprotin_nums.append(int(word[0][1]))
    # print(len(sprotin_nums), len(set(sprotin_nums)))
    # num list converted to set
    sprotin_nums = set(sprotin_nums)
    missing_nums = []
    for num in range(len(sprotin_nums)):
        if num not in sprotin_nums:
            missing_nums.append(num)
        
    print('Highest ID from Sprotin:', max(sprotin_nums))    
    print('No. of IDs from Sprotin:', len(sprotin_nums))
    print('No. of IDs missing from Sprotin:', len(missing_nums))
    
    return sprotin_nums
    

def join_to_string(SH_list):
    
    string_list = []
    
    for word in SH_list:
        joined_word = [';'.join([str(item) for item in word_form]) for word_form in word]
        string_list.append(joined_word)
        
    return string_list

if __name__ == '__main__':
    
    SHsnid_folder = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None
    
    manual_paradigm_dir = 'FO_inflection_data/manual_paradigms'
    
    if os.path.isdir(manual_paradigm_dir):
        print('\nCopying manual paradigm files over...')
        for file_handle in os.listdir(manual_paradigm_dir):
            print('> ' + file_handle)
            shutil.copy(os.path.join(manual_paradigm_dir, file_handle), SHsnid_folder)
        print('Files copied\n')
    
    SH = get_all_SHsnid_words(SHsnid_folder)
    ID_set = get_stats_and_ID_set(SH)
    enumerated_SH = enumerate_and_rename_words(SH, ID_set)
    renamed_SH = rename_classes(enumerated_SH)
    SH_strings = join_to_string(enumerated_SH)
    
    with open(output_file, 'w') if output_file else sys.stdout as out:
        for word in SH_strings:
            for form in word:
                if ';-;' not in form:
                    out.write(form)
                    out.write('\n')
