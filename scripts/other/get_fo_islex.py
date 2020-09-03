
import re
import os

from collections import defaultdict
from pprint import pprint


class Node:
    def __init__(self, indented_line):
        self.children = []
        self.level = len(indented_line) - len(indented_line.lstrip())
        self.text = indented_line.strip()

    def add_children(self, nodes):
        childlevel = nodes[0].level
        while nodes:
            node = nodes.pop(0)
            if node.level == childlevel: # add node as a child
                self.children.append(node)
            elif node.level > childlevel: # add nodes as grandchildren of the last child
                nodes.insert(0,node)
                self.children[-1].add_children(nodes)
            elif node.level <= self.level: # this node is a sibling, no more children
                nodes.insert(0,node)
                return

    def as_dict(self):
        if len(self.children) > 1:
            return {self.text: [node.as_dict() for node in self.children]}
        elif len(self.children) == 1:
            return {self.text: self.children[0].as_dict()}
        else:
            return self.text


RE_LEMMA_NR = r'(?<=FLETTA\()\d*(?=\))'
RE_IS_LEMMA = r'^[0-9A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\- .,/]*(?=; )'
RE_FO_LEMMA = r'FO-[A-Za-zþæðÆÐØøáéýúíóÁÉÝÚÍÓ ]*: [A-Za-zþæðÆÐØøáéýúíóÁÉÝÚÍÓ /]*'
RE_FO_LEMMA_LABEL = r'FO-[A-Za-zþæðÆÐØøáéýúíóÁÉÝÚÍÓ ]*: '
RE_WCLASS = r'(?<=; ).*(?=;( |\n))'
RE_BRANCH = r'LIÐUR'
RE_MWE = r'SOSTÆÐA'

lemmas = []

with open('../corpora/islex/faereyska-a-o.txt') as FO:
    lemma_info = ''
    for line in FO.readlines():
        if line == '\n':
            continue
        elif re.search(r'FLETTA', line):
            if len(lemma_info.split('\n')) > 2:
                lemmas.append(lemma_info)
                lemma_info = ''
            else:
                lemma_info = ''
        line = re.sub(r'^    \b', '\t', line)
        line = re.sub(r'^        \b', '\t\t', line)
        line = re.sub(r'^          \b', '\t\t', line)
        line = re.sub(r'^            \b', '\t\t', line)
        line = re.sub(r'^                \b', '\t\t\t', line)
        line = re.sub(r'^                    \b', '\t\t\t', line)
        # line = re.sub(r'^                        \b', '\t\t\t', line)
        line = re.sub(r'^                            \b', '\t\t\t\t', line)
        lemma_info += line

# for entry in lemmas:
#     entry_dict = defaultdict(lambda defaultdict(list))
#     print(entry)
#     PARENT_BRANCH = None
#     for line in entry.splitlines(keepends=True):
#         level = len(re.search(r'^\s*\b', line)[0])
#         # print(level)
#         if level == 0:
#             # print('level 0')
#             # print(line.split(': '))
#             lemma_nr = re.search(r'\d+', line.split(': ')[0])[0]
#             lemma = re.search(RE_IS_LEMMA, line.split(': ')[1])[0]
#             wclass = re.search(RE_WCLASS, line.split(': ')[1])[0]
#             entry_dict.update({'id': lemma_nr, 'lemma': lemma, 'class': wclass})
#         elif level == 1:
#             key = re.sub(r'^\d+ ', '', line.split(': ')[0].strip('\t'))
#             value = line.split(': ')[1]
#
#             if key == 'LIÐUR':
#                 PARENT_BRANCH = value
#             else:
#                 entry_dict[key].append(value.strip('\n'))
#         elif level == 2:
#             if PARENT_BRANCH:
#                 key = re.sub(r'^\d+ ', '', line.split(': ')[0].strip('\t'))
#                 value = line.split(': ')[1]
#                 entry_dict['LIÐUR'][PARENT_BRANCH].append({})

        # print(len(begin_whitespace))

    # print(entry_dict)
    # input()
    # for i in
    # entry_dict[lemma_nr].{'lemma'
    # input()

for entry in lemmas:
    print(entry)
    root = Node('root')
    root.add_children([Node(line) for line in entry.splitlines() if line.strip()])
    d = root.as_dict()['root']
    pprint(d)
    input()


'''
    if re.search(RE_BRANCH, entry):
        print(entry)

        lemma_nr = re.search(RE_LEMMA_NR, entry)[0]
        is_lemma = re.search(RE_IS_LEMMA, entry)[0]

        entry_lines = entry.splitlines(keepends=True)
        branches = []
        branch = ''
        for line in entry_lines:
            if re.search(r'FLETTA', line):
                continue
            elif re.search(r'LIÐUR', line):
                if len(branch.split('\n')) > 2:
                    branches.append(branch)
                    branch = ''
                # else:
                #     branch = ''
            branch += line
        print(len(branches))
        for branch in branches:
            print(branch)
        input()
        continue
        # TODO: add nice way to deal with branched entry
    elif re.search(RE_MWE, entry):
        # print('\nMWE\n')
        continue
        # TODO: add nice way to deal with MWE entry

    continue
    lemma_nr = re.search(RE_LEMMA_NR, entry)[0]
    wclass = re.search(RE_WCLASS, entry)[0]
    is_lemma = re.search(RE_IS_LEMMA, entry)[0]
    fo_lemma = re.sub(RE_FO_LEMMA_LABEL, '', re.search(re_fo_lemma, entry)[0])
    print('Nr:', lemma_nr)
    print('IS lemma:', is_lemma)
    print('FO lemma:', fo_lemma)
    # input()
'''
