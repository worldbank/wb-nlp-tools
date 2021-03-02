# WB Cleaning Module

This module contains the implementation for a suite of text preprocessing and cleaning pipeline. The cleaning architecture is designed to be flexible and can be configured through config files, e.g., [`configs/cleaning/default.yml`](configs/cleaning/default.yml).

# Modules

### Document preprocessing and cleaning

Most of the raw data that we are using are in the form of PDF and text documents. We develop a suite of preprocessing and cleaning modules to handle the transformations required to generate a high quality input to our models.

An overview of the pipeline is as follows:
- Convert pdf to text
- Parse the text document and perform sentence tokenization.
- Lemmatize the tokens and remove stop words.
- Drop all non-alphabetical tokens.
- Apply spell check and try to recover misspelled words.
- Normalize tokens by converting to lowercase.

### Phrase detection

Part of the preprocessing is also the inference of phrases in the documents. Phrases are logical grouping of tokens that represent an intrinsic meaning.

We are primarily leveraging the [Gensim](https://radimrehurek.com/gensim/) NLP toolkit and Spacy to develop the phrase detection algorithms.

### Acronym detection

Acronyms are fairly common in documents from development organizations and multilateral development banks. In this project, we include in our pipeline an acronym detector and expander. The idea is to detect acronyms in a document and replace all of the acronyms with the appropriate expansion.

We also keep track of multiple instances of an acronym and generate prototypes for each that encodes the information of the acronym, e.g., PPP -> private-public partnership or purchasing power parity.
