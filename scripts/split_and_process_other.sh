#!/bin/bash

# ex. usage: scripts/split_and_process_other.sh corpora/tagged_corpus_sosialurin/fo.revised.txt sosialurin_revised
# corpora/MIM-GOLD.20.05/13_categories/fbl.txt
if [[ $# -eq 0 ]] ; then
    echo 'Usage: '$0' path/to/corpus.txt version_name'
    exit 0
fi

IN_FILE=$1
VERSION=$2
PROCESSED_FOLDER="$(dirname "$IN_FILE")"/processed

# split into 10 folds
echo
echo "Splitting into folds..."
# python3 scripts/split_fold.py corpora/tagged_corpus_sosialurin/fo.revised.txt 10 revised
python3 scripts/corpus_stuff/nth_split_fold.py $IN_FILE 10 $VERSION
echo "Folds ready!"
echo

# make output in tagger directory

if [ -d ./utils/ABLTagger/data/$VERSION ]
then
  rm -r ./utils/ABLTagger/data/$VERSION
  mkdir -p ./utils/ABLTagger/data/$VERSION
else
  mkdir -p ./utils/ABLTagger/data/$VERSION
fi


echo "Processing fold files for tagger..."
for i in 01 02 03 04 05 06 07 08 09 10
do
  python3 ./utils/ABLTagger/preprocess/generate_coarse_training_set.py -i ./$PROCESSED_FOLDER/10_fold_$VERSION/${i}TM.txt -o ./utils/ABLTagger/data/$VERSION/${i}TM_word_class.txt
  python3 ./utils/ABLTagger/preprocess/generate_coarse_training_set.py -i ./$PROCESSED_FOLDER/10_fold_$VERSION/${i}PM.txt -o ./utils/ABLTagger/data/$VERSION/${i}PM_word_class.txt
  python3 ./utils/ABLTagger/preprocess/generate_fine_training_set.py -i ./$PROCESSED_FOLDER/10_fold_$VERSION/${i}TM.txt -o ./utils/ABLTagger/data/$VERSION/${i}TM.txt
  python3 ./utils/ABLTagger/preprocess/generate_fine_training_set.py -i ./$PROCESSED_FOLDER/10_fold_$VERSION/${i}PM.txt -o ./utils/ABLTagger/data/$VERSION/${i}PM.txt
  # echo "Fold $i processed..."
done
echo "Folds processed!" 
echo

echo "Uploading output folder to dropbox..."
./utils/Dropbox-Uploader/dropbox_uploader.sh delete far/$VERSION
./utils/Dropbox-Uploader/dropbox_uploader.sh upload ./utils/ABLTagger/data/$VERSION far/

echo "All done!"
