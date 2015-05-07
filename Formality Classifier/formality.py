import os, sys, re, nltk, enchant, random
import simplejson as json
import xml.etree.ElementTree as ET
from nltk.corpus import nps_chat
from nltk.classify.naivebayes import NaiveBayesClassifier as learner

english = enchant.Dict("en_US")
SUBJECT_CHARS = 50


class FormalityClassifier:
    """Classify text based on the formality of the formatting and content"""

    def build_informal_set(self):
        #
        labeled_sets = []
        path = os.path.join(self.curdir, "data/enron/training set/informal")
        #print "Informal"
        for filename in os.listdir(path):
            if filename == ".DS_Store":
                continue
            file = path + "/" + filename
            #print file
            msg = ""
            for line in open(file,'r'):
                msg = msg + " " + line
            labeled_sets.append((self.extract_features(msg), self.informal_label))
        return labeled_sets

    def build_formal_set(self):
        labeled_sets = []
        path = os.path.join(self.curdir, "data/enron/training set/formal")
        #print "Formal"
        for filename in os.listdir(path):
            if filename == ".DS_Store":
                continue
            file = path + "/" + filename
            #print file
            msg = ""
            for line in open(file,'r'):
                msg = msg + " " + line
            labeled_sets.append((self.extract_features(msg), self.formal_label))
        return labeled_sets

    def test_self(self):
        correct = 0
        pos_correct = 0
        neg_correct = 0
        false_formal = 0
        false_informal = 0
        for (example, label) in self.labeled_features:
            if self.classifier.classify(example) == label:
                correct += 1
                if label == self.formal_label: pos_correct += 1
                if label == self.informal_label: neg_correct += 1
            else:
                if label == self.formal_label: false_informal += 1
                if label == self.informal_label: false_formal += 1
        print correct, " / ", len(self.labeled_features)
        print "formal correct: ", pos_correct
        print "informal correct: ", neg_correct
        print "false formal: ", false_formal
        print "false informal: ", false_informal

    def build_classifier(self):
        #print "Informal"
        self.labeled_features = self.build_informal_set()
        #print "Formal"
        self.labeled_features.extend(self.build_formal_set())
        classifier = learner.train(self.labeled_features)
        #classifier.show_most_informative_features()
        return classifier

    def get_classifier(self):
        return self.classifier

    def get_true_value(self):
        return self.formal_label

    def file_to_list(self, filename):
        try:
            lines = [line.strip() for line in file(filename).readlines()]
        except:
            print "--- WARNING: Needs %s to be in the same directory as formality.py" % (filename)
            return []
        return lines

    def classification_format(self, raw, subject=None):
        msg = nltk.clean_html(raw)
        fs = self.extract_features(msg, subject)
        return fs

    def classify(self, raw, subject=None):
        return self.classifier.classify(self.classification_format(raw, subject))

    def prob_classify(self, raw, subject=None):
        dist = self.classifier.prob_classify(self.classification_format(raw, subject))
        return dist.prob(dist.max())

    def extract_features(self, msg, subj=None):
        # features:
        # 	portion of words capitalized properly
        # 	occurrence of swear words, emoticons, and
        # 	number of misspelled words (real but not spelled correctly)
        #print len(msg)
        words = nltk.word_tokenize(msg)
        messy_words = msg.rsplit()
        counts = {}
        weights = {}
        features = {}
        counts["capitalized"] = 0
        counts["emoticons"] = 0
        counts["abbreviations"] = 0
        counts["slurs"] = 0
        counts["swears"] = 0
        counts["misspelled"] = 0
        counts["subject_capitalized"] = 0
        counts["negative"] = 0
        counts["informal_words"] = 0
        counts["informal_punctuation"] = 0
        counts["formal_punctuation"] = 0
        counts["polite"] = 0
        wordcount = len(words)
        if wordcount is 0: wordcount = 1
        for word in words:
            if word == word.capitalize():
                counts["capitalized"] += 1.0
            else:  # don't check capitalized words for spelling as they're likely to be proper nouns
                if not english.check(word): counts["misspelled"] += 1.0
            word = word.lower()
            if word in self.swears: counts["swears"] += 1.0
            if word in self.negative: counts["negative"] += 1.0
            if word in self.informal_words: counts["informal_words"] += 1.0
            if word in self.informal_punctuation: counts["informal_punctuation"] += 1.0
            if word in self.formal_punctuation: counts["formal_punctuation"] += 1.0
            if word in self.polite: counts["polite"] += 1.0
            if word in self.abbreviations: counts["abbreviations"] += 1.0
            lastchar = ''
            streak = 1
            for char in word:
                if streak > 2:
                    counts["slurs"] += 1.0
                    break
                if lastchar == char:
                    streak += 1
                else:
                    lastchar = char

        features["msg_length"] = (len(msg)>1000)
        features["swears"] = (counts["swears"] > 0)
        features["emoticons"] = (counts["emoticons"] > 0)
        features["abbreviations"] = (counts["abbreviations"] > 0)
        features["slurs"] = (counts["slurs"] > 0)
        features["informal_words"] = (counts["informal_words"] > 0)
        features["informal_punctuation"] = (counts["informal_punctuation"] > 0)
        features["formal_punctuation"] = (counts["formal_punctuation"] > 0)
        features["polite"] = (counts["polite"] > 0)
        features["negative"] = (counts["negative"] > 0)
        features["misspelled"] = (counts["misspelled"] > 1)
        features["capitalized"] = (counts["capitalized"] / wordcount > 0.07)
        return features

    def __init__(self):
        self.curdir = os.path.dirname(os.path.realpath(__file__))
        self.formal_label = "formal"
        self.informal_label = "informal"
        self.swears = self.file_to_list(os.path.join(self.curdir, "data/informal/swears"))
        self.emoticons = self.file_to_list(os.path.join(self.curdir, "data/informal/emoticons"))
        self.abbreviations = self.file_to_list(os.path.join(self.curdir, "data/informal/abbreviations"))
        self.negative = self.file_to_list(os.path.join(self.curdir, "data/informal/negative"))
        self.informal_words = self.file_to_list(os.path.join(self.curdir, "data/informal/informal_words"))
        self.informal_punctuation = self.file_to_list(os.path.join(self.curdir, "data/informal/informal_punctuation"))
        self.formal_punctuation = self.file_to_list(os.path.join(self.curdir, "data/formal/formal_punctuation"))
        self.polite = self.file_to_list(os.path.join(self.curdir, "data/formal/polite"))
        self.classifier = self.build_classifier()
        #self.test_self() #Check trained classifier


def main():
    f = FormalityClassifier()
    classifier = f.get_classifier() #trained classifier
    print classifier.show_most_informative_features()
    print "Training done\n"
    '''
    path = os.path.join(f.curdir, "data/enron/test answers")
    formal = []
    for line in open(path+"/formal.txt","r"):
        formal.append(line.strip())
    informal = []
    for line in open(path+"/informal.txt","r"):
        informal.append(line.strip())
    '''
    path = os.path.join(f.curdir, "data/enron/final_non_requests")
        #print "Informal"
    '''
    correct_formal = 0
    correct_informal = 0
    false_formal = 0
    false_informal = 0
    '''
    for filename in os.listdir(path):
        if filename == ".DS_Store":
            continue
        file = path + "/" + filename
        #print file
        msg = ""
        for line in open(file,'r'):
            msg = msg + " " + line
        featureset = f.extract_features(msg.strip())
        predicted_label = classifier.classify(featureset)
        print filename,predicted_label #naivebayes object
        '''
        if predicted_label == "formal":
            if filename in formal:
                correct_formal += 1
                print "correct\n"
            else:
                false_formal +=1
                print "incorrect\n"

        else:
            if filename in informal:
                correct_informal += 1
                print "correct\n"
            else:
                false_informal +=1
                print "incorrect\n"

    accuracy = (float)(correct_formal+correct_informal)/(len(formal)+len(informal))
    print accuracy*100,"%"
    print correct_formal,false_formal,correct_informal,false_informal
    '''

if __name__ == "__main__":
    main()