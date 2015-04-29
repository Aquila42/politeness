__author__ = 'rishina'

#getting bigrams to fill in the bigrams_formal and bigrams_informal

import nltk,os
from nltk import word_tokenize
from nltk.util import ngrams

# formal bigrams
writeFile = open('/Users/rishina/desktop/politeness/Formality Classifier/data/formal/bigrams_formal.txt', 'w')
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
        bigrams = ngrams(lower_words,2)
        string = ''
        for bigram in bigrams:
                string = str(bigram)
                string = string + '\n'
                writeFile.write(string)


#informal bigrams

writeFile = open('/Users/rishina/desktop/politeness/Formality Classifier/data/informal/bigrams_informal.txt', 'w')
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
        bigrams = ngrams(lower_words,2)
        string = ''
        for bigram in bigrams:
                string = str(bigram)
                string = string + '\n'
                writeFile.write(string)

