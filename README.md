
# Faroese implementation of ABLTagger

This repository contains data, models, and scripts used to train and evaluate [ABLTagger](https://github.com/steinst/ABLTagger), a BiLSTM based neural PoS tagger, on Faroese. 

Using the ~100.000 token Sosialurin corpus with a revised tagging scheme and an experimental morphological database for Faroese, the trained model acheives an overall accuracy of 91.40% when evaluated using 10-fold cross validation.


## Contents
This repo has three folders:
#### Sosialurin corpus

The [Sosialurin corpus](http://ark.axeltra.com/index.php?type=person|lng=en|id=18), originally compiled in 2004 and revised in 2011, was pre-processed for this project to various degrees and several versions are provided here:

- Whole corpus files:
  - `original.txt` - The corpus unchanged from 2004/2011
  - `fo.txt` - Comments removed and whitespace issues
  - `fo.cleaned.txt` - Tokenization issues fixed and newlines added
  - `fo.revised-verbs-unchanged.txt` - Same as above, with revised tagset except for plural verbs
  - `fo.revised.txt` - Fully revised tagset and tokenization
- 10 fold splits of three versions of the corpus (for cross validation)
- Tagset descriptions - Both original and revised
- Original license waiver from 2011
- Description of contents

#### Inflection data

As ABLTagger makes use of a morphological database in the [DIM basic format](https://bin.arnastofnun.is/DMII/LTdata/s-format/), an Experimental Database of Faroese Morphology (EDFM) was compiled from various sources and formatted in this manner, in order to use with ABLTagger. The EDFM contains about 1.000.000 inflectional forms in 67,180 individual paradigms. This is contained within the file `edfm.csv`.

The contents of EDFM are described below. The sources of inflectional paradigms were the Faroese dictionary foundation (OBG), the Faroese naming committee (Navnanevndin) and Wiktionary (via [UniMorph](https://unimorph.github.io/)). Additionally paradigms were generated from OBG data using scripts (OBG-gen) and various paradigms, mostly non-inflecting words, were created manually. The OBG and Navnanevndin paradigms were accessed via [Sprotin.fo](www.sprotin.fo)

| Word class | OBG | Navnanevndin | Wiktionary | OBG-gen | Manual | Total | 
|-------------------|:------:|:-----:|:---:|:-----:|:---:|:-------:|
| **Adjectives**    | 11,907 | -     | 16  | -     | -   | 11,923  |
| **Adverbs**       | 1,289  | -     | -   | -     | -   | 1,289   |
| **Conjunctions**  | -      | -     | -   | -     | 61  | 6       |
| **Interjections** | -      | -     | -   | -     | 115 | 115     |
| **Nouns**         | 46,492 | 1,667 | 113 | -     | -   | 48,272  |
| **Numerals**      | -      | -     | -   | 47    | 57  | 104     |
| **Prepositions**  | -      | -     | -   | -     | 62  | 62      |
| **Pronouns**      | -      | -     | -   | -     | 20  | 20      |
| **Verbs**         | -      | -     | 7   | 5,327 | -   | 5,334   |
| **Total**         | 59,688 | 1,667 | 136 | 5,374 | 315 | **67,180** | 

#### Scripts used

The various scripts used in all stages of the project are in the `scripts` folder. These are ordered into three groups, into `inflection`, `tagset` and `corpus_stuff`, indicating what the scripts were used for. Other than that, they are not organized specifically

#### Models

The Faroese-trained models, to be used with ABLTagger in tandem with EDFM are kept here.
