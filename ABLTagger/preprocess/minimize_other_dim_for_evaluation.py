import sys

data_folder = 'utils/ABLTagger/data/' + sys.argv[1] + '/'
dim_folder = 'utils/ABLTagger/extra/'
train_test_files = ['01PM.txt', '01TM.txt', '02PM.txt', '02TM.txt', '03PM.txt', 
                    '03TM.txt', '04PM.txt', '04TM.txt', '05PM.txt', '05TM.txt', 
                    '06PM.txt', '06TM.txt', '07PM.txt', '07TM.txt', '08PM.txt', 
                    '08TM.txt', '09PM.txt', '09TM.txt', '10PM.txt', '10TM.txt']
training_set = sys.argv[1]
dim_in = 'dmii.vectors'
dim_out = 'dmii.vectors.' + training_set

training_dict = {}
for i in train_test_files:
    curr_file = open(data_folder + i, 'r')
    training_lines = curr_file.readlines()
    for j in training_lines:
        try:
            word_split = j.split()
            training_dict[word_split[0]] = 1
        except:
            pass

print(len(training_dict))
dim_file = open(dim_folder + dim_in, 'r')
dim_lines = dim_file.readlines()

with open(dim_folder + dim_out, "w") as f:
    for dim_wordform in dim_lines:
        try:
            temp = dim_wordform.split(';')[0]
            if temp in training_dict.keys():
                f.write(dim_wordform)
        except:
            pass
