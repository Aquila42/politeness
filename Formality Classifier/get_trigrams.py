__author__ = 'rishina'

#getting trigrams to fill in the trigrams_formal and trigrams_informal

import nltk,os
from nltk import word_tokenize
from nltk.util import ngrams

# formal trigrams
writeFile = open('/Users/rishina/desktop/politeness/Formality Classifier/data/formal/trigrams_formal.txt', 'w')
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
        trigrams = ngrams(lower_words,3)
        string = ''
        for trigram in trigrams:
                string = str(trigram)
                string = string + '\n'
                writeFile.write(string)


#informal trigrams

writeFile = open('/Users/rishina/desktop/politeness/Formality Classifier/data/informal/trigrams_informal.txt', 'w')
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
        trigrams = ngrams(lower_words,3)
        string = ''
        for trigram in trigrams:
                string = str(trigram)
                string = string + '\n'
                writeFile.write(string)

