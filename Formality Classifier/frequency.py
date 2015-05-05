__author__ = 'Aquila'
import os
import nltk
import operator

path = os.path.join(os.curdir, "data/enron/training set/informal")
msg = ""
for filename in os.listdir(path):
    if filename == ".DS_Store":
        continue
    file = path + "/" + filename
    for line in open(file,'r'):
        msg = msg + " " + line

words = nltk.word_tokenize(msg.lower())
counts = {}
for word in words:
    if word not in counts:
        counts[word] = 1
    else:
        counts[word] += 1

print sorted(counts.items(),key=operator.itemgetter(1))[::-1]

'''
for word in counts.keys():
    if counts[word] > 100:
        print word

'''