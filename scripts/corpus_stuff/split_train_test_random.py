import sys
# import argparse
import random
import re



def main():
    # '../corpora/tagged_corpus_sosialurin/sosialurin_corpus_IStag.txt'
    FILE = sys.argv[1]
    TEST_PERCENTAGE = 10

    all_sents = []

    with open(FILE, 'r') as file:
        sentence = []
        lines = file.readlines()
        for line in lines:
            sentence.append(line)
            if line == '\n':
                all_sents.append(sentence)
                sentence = []

    total_sent_num = len(all_sents)

    test_sent_num = int(round(total_sent_num / TEST_PERCENTAGE))
    train_sent_num = total_sent_num - test_sent_num

    print(f'\nTotal number of sentences: {total_sent_num}')
    sent_lengths = [len(i) for i in all_sents]
    print(f'Total number of tokens: {sum(sent_lengths)}\n')


    train = all_sents
    test = [train.pop(random.randrange(len(train))) for _ in range(test_sent_num)]

    assert len(test) == test_sent_num
    assert len(train) == train_sent_num

    print(f'Train sentences: {train_sent_num}')
    train_lengths = [len(i) for i in train]
    print(f'Train tokens: {sum(train_lengths)}\n')
    print(f'Test sentences: {test_sent_num}')
    test_lengths = [len(i) for i in test]
    print(f'Test tokens: {sum(test_lengths)}\n')

    with open(re.sub(r'\.txt', '.train', FILE), 'w') as train_file,\
        open(re.sub(r'\.txt', '.test', FILE), 'w') as test_file:
        for sent in train:
            for token in sent:
                train_file.write(token)
            train_file.write('\n')
        for sent in test:
            for token in sent:
                test_file.write(token)
            test_file.write('\n')

if __name__ == '__main__':
    main()
