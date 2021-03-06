__author__ = 'rishina'

#getting unigrams to fill in the unigrams_formal and unigrams_informal

import nltk,os
from nltk import word_tokenize
from nltk.util import ngrams

# formal unigrams
writeFile = open('/Users/rishina/desktop/politeness/Formality Classifier/data/formal/unigrams_formal.txt', 'w')
path = "/Users/rishina/desktop/politeness/Formality Classifier/data/enron/training set/formal"
for filename in os.listdir(path):
        if filename == ".DS_Store":
                continue
        file = path + "/" + filename
        #print file
        msg = ""
        for line in open(file,'r'):
                msg = msg + " " + line
        lower_words = nltk.word_tokenize(msg.lower())
        unigrams = ngrams(lower_words,1)
        string = ''
        for unigram in unigrams:
                string = str(unigram)
                string = string + '\n'
                writeFile.write(string)


#informal unigrams

writeFile = open('/Users/rishina/desktop/politeness/Formality Classifier/data/informal/unigrams_informal.txt', 'w')
path = "/Users/rishina/desktop/politeness/Formality Classifier/data/enron/training set/informal"
for filename in os.listdir(path):
        if filename == ".DS_Store":
                continue
        file = path + "/" + filename
        #print file
        msg = ""
        for line in open(file,'r'):
                msg = msg + " " + line
        lower_words = nltk.word_tokenize(msg.lower())
        unigrams = ngrams(lower_words,1)
        string = ''
        for unigram in unigrams:
                string = str(unigram)
                string = string + '\n'
                writeFile.write(string)

