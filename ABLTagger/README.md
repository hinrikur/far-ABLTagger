# far-ABLTagger

This is a Faroese Implementation of [ABLTagger](https://github.com/steinst/ABLTagger), a bidirectonal LSTM Part-of-Speech Tagger with combined Word and Character embeddings, augmented with a morphological lexicon and a lexical category identification step. The ABLTagger system is described in the paper [Augmenting a BiLSTM Tagger with a Morphological Lexicon and a Lexical Category Identification Step](https://www.aclweb.org/anthology/R19-1133/). The Faroese implementation is described in the MA thesis [A Faroese part-of-speech tagger built with Icelandic methods: Data preperation, training and evaluation](https://skemman.is/handle/1946/37025).

This folder contains the ABLTagger system, configured for **tagging** Faroese text, using the provided model. For training and evaluating, the same parameters are used as in original ABLTagger release, as described in [its GitHub repository](https://github.com/steinst/ABLTagger).


## Tagging texts
Texts can be tagged using the script `tag.py`. The program loads a model stored in the `./models` folder. By default, the model provided is trained on the ~100,000 word Sosialurin corpus with the revised Faroese tagset. 

<!-- * Full
    - A model trained on all training data used in the paper cited above, taking advantage of the whole DMII morphological lexicon. This model needs at least 16GB RAM to load.
    - Download link: https://www.dropbox.com/s/59thds6lun2zki5/Full.tar.gz?dl=0 (374 MB download - 7.0 GB uncompressed)
    - The model should go into a folder called ./models/Full -->
    
* **SosBR** - A model trained on the Faroese Sosialurin corpus, with the revised Faroese tagset, with the EDFM as the morphological component.

<!-- The model needs the contents of https://www.dropbox.com/s/97s4zk4d9zk722x/extra.tar.gz?dl=0 to be in the ./extra folder. -->

Running `./tag.py -h` gives information on all possible parameters. At minimum the input file(s) have to be specified, and normally the model is also specified. 

**Note:** Input files must contain tokenized text, one sentence per line. The Reynir tokenizer is not configured for tokenizing Faroese, but may be used in a pinch for somewhat good results.

```
python3 ./tag.py -m SosBR -i text_file.txt
```

| Required Parameters                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -i --input 	       |	None           | File(s) to tag. Files should include tokenized sentences. One sentence per line. Each token followed by whitespace.

| Optional Parameters                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -m --model 	       |	SosBR           | Select model. It should be stored in ./models/[model-name]/
| -o --output 	       |	.tagged           | Select suffix for output files.
| -type --tag_type 	       |	combined           | Select tagging type: coarse, fine or combined'.
| --tokenize 	       |	None           | Use the Reynir tokenizer to tokenize input text. Action is invoked by using the parameter. 

<!-- ## Evaluating models
Training/testing sets can be evaluated with the script `evaluate.py`. Before evaluation a script to minimize the DIM, `minimize_dim_for_evaluation.py`, can be run to reduce time spent in training and testing the model. The script finds all word forms in the training/testing data and removes n-hot vectors from the DIM file for words that are not in the training/testing data.
Before evaluating the models the `./preprocess/generate_fine_training_set.py` and `./preprocess/generate_coarse_training_set.py` should be run as described in the previous section, on all train/test files.
To evaluate the accuracy of the tagger on fold number 1 in a set of 10 folds from the mim_gold corpus, the following command does that with all the same settings as used in the paper.
```
python3 ./evaluate.py -c mim_gold -fold 1 -morphles dmii.vectors.mim_gold
```
Running `./evaluate.py -h` gives information on all possible parameters.

| Optional Parameters                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -o --optimization 	       |	SimpleSGD           | Optimization algorithm to use. Available algorithms are: SimpleSGD, MomentumSGD, CyclicalSGD, Adam, RMSProp.
| -lr --learning_rate 	       |	0.13           | Learning rate
| -lrd --learning_rate_decay 	       |	0.05           | Learning rate decay
| -l_max --learning_rate_max 	       |	0.1           | Learning rate max for Cyclical SGD
| -l_min --learning_rate_min 	       |	0.01           | Learning rate min for Cyclical SGD
| -d --dropout 	       |	0.0           | Dropout rate
| -data --data_folder 	       |	./data/           | Folder containing training data.
| -morphlex --use_morphlex 	       |	None           | File with morphological lexicon embeddings in ./extra folder.
| -load_chars --load_characters 	       |	./extra/characters_training.txt           | File to load characters from
| -load_coarse --load_coarse_tagset 	       |	./extra/word_class_vectors.txt           | Load embeddings file for coarse grained tagset
| -coarse --coarse_type 	       |	word_class           | Select type of coarse data.
| -type --training_type 	       |	combined           | Select training type: coarse, fine or combined.
| -c --corpus 	       |	otb           | Name of training corpus
| -fold --dataset_fold 	       |	1           | select which dataset to use (1-10)
| -ecg --epochs_coarse_grained 	       |	12           | Number of epochs for coarse grained training.
| -efg --epochs_fine_grained 	       |	20           | Number of epochs for fine grained training.
| -n --noise 	       |	0.1           | Noise in embeddings

The script writes results to files in the `./evaluate/` folder. `./preprocess/calc_accuracy.py` reads these files and gives you the average accuracy over all the folds in a 10-fold validation. `./preprocess/quantify_errors.py` gives you a list of the most common errors made by the tagger. -->
