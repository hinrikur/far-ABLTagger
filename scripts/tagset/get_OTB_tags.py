
import os

FILES = ['01PM.txt',
         '01TM.txt',
         '02PM.txt',
         '02TM.txt',
         '03PM.txt',
         '03TM.txt',
         '04PM.txt',
         '04TM.txt',
         '05PM.txt',
         '05TM.txt',
         '06PM.txt',
         '06TM.txt',
         '07PM.txt',
         '07TM.txt',
         '08PM.txt',
         '08TM.txt',
         '09PM.txt',
         '09TM.txt',
         '10PM.txt',
         '10TM.txt',]

PATH = '../utils/Djupavik/IFD'

for file in FILES:
    with open(os.path.join(PATH, file)) as f:
        for line in f.readlines():
            print(line)
