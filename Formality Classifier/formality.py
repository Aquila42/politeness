import os, sys, re, nltk, enchant, random
from nltk.util import ngrams
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
        # print "Informal"
        for filename in os.listdir(path):
            if filename == ".DS_Store":
                continue
            file = path + "/" + filename
            #print file
            msg = ""
            for line in open(file, 'r'):
                msg = msg + " " + line
            labeled_sets.append((self.extract_features(msg), self.informal_label))
        return labeled_sets

    def build_formal_set(self):
        labeled_sets = []
        path = os.path.join(self.curdir, "data/enron/training set/formal")
        # print "Formal"
        for filename in os.listdir(path):
            if filename == ".DS_Store":
                continue
            file = path + "/" + filename
            #print file
            msg = ""
            for line in open(file, 'r'):
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
        self.labeled_features = self.build_informal_set()
        self.labeled_features.extend(self.build_formal_set())
        classifier = learner.train(self.labeled_features)
        # classifier.show_most_informative_features()
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
        # portion of words capitalized properly
        # 	occurrence of swear words, emoticons, and
        # 	number of misspelled words (real but not spelled correctly)
        words = nltk.word_tokenize(msg)
        if subj is None:
            if len(msg) < SUBJECT_CHARS:
                subj = msg
            else:
                subj = msg[:50]
        subject = nltk.word_tokenize(subj)
        messy_words = msg.rsplit()
        counts = {}
        weights = {}
        features = {}

        #counts["unigrams_formal"] = 0
        counts["bigrams_formal"] = 0
        counts["trigrams_formal"] = 0
        #counts["unigrams_informal"] = 0
        counts["bigrams_informal"] = 0
        counts["trigrams_informal"] = 0

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

        lower_words = nltk.word_tokenize(msg.lower())
        #unigrams = ngrams(lower_words, 1)
        bigrams = ngrams(lower_words, 2)
        trigrams = ngrams(lower_words, 3)
        #for unigram in unigrams:
        #    unigram = str(unigram)
        #    if unigram in self.unigrams_formal: counts["unigrams_formal"] += 1.0
        #    if unigram in self.unigrams_informal: counts["unigrams_informal"] += 1.0
        for bigram in bigrams:
            bigram = str(bigram)
            if bigram in self.bigrams_formal: counts["bigrams_formal"] += 1.0
            if bigram in self.bigrams_informal: counts["bigrams_informal"] += 1.0
        for trigram in trigrams:
            trigram = str(trigram)
            if trigram in self.trigrams_formal: counts["trigrams_formal"] += 1.0
            if trigram in self.trigrams_informal: counts["trigrams_informal"] += 1.0

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
        for word in messy_words:
            if word in self.emoticons: counts["emoticons"] += 1.0
        for word in subject:
            if word.lower() == 're' or word.lower() == 'fwd': continue
            if word == word.capitalize() and word.isalpha():
               counts["subject_capitalized"] += 1.0

        #features["unigrams_formal"] = (counts["unigrams_formal"] > 0)
        features["bigrams_formal"] = (counts["bigrams_formal"] > 0)
        features["trigrams_formal"] = (counts["trigrams_formal"] > 0)
        #features["unigrams_informal"] = (counts["unigrams_informal"] > 0)
        features["bigrams_informal"] = (counts["bigrams_informal"] > 0)
        features["trigrams_informal"] = (counts["trigrams_informal"] > 0)

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
        features["subject_capitalized"] = (counts["subject_capitalized"] > 1)
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

        #self.unigrams_formal = self.file_to_list(os.path.join(self.curdir, "data/formal/unigrams_formal.txt"))
        self.bigrams_formal = self.file_to_list(os.path.join(self.curdir, "data/formal/bigrams_formal.txt"))
        self.trigrams_formal = self.file_to_list(os.path.join(self.curdir, "data/formal/trigrams_formal.txt"))
        #self.unigrams_informal = self.file_to_list(os.path.join(self.curdir, "data/informal/unigrams_informal.txt"))
        self.bigrams_informal = self.file_to_list(os.path.join(self.curdir, "data/informal/bigrams_informal.txt"))
        self.trigrams_informal = self.file_to_list(os.path.join(self.curdir, "data/informal/trigrams_informal.txt"))

        self.classifier = self.build_classifier()
        self.test_self() #Check trained classifier


def main():
    f = FormalityClassifier()
    classifier = f.get_classifier()  # trained classifier
    print classifier.show_most_informative_features()
    print "Training done\n"
    path = os.path.join(f.curdir, "data/enron/test answers/")
    formal = []
    for line in open(path + "/formal.txt", "r"):
        formal.append(line.strip())
    informal = []
    for line in open(path + "/informal.txt", "r"):
        informal.append(line.strip())
    path = os.path.join(f.curdir, "data/enron/test set/")
    # print "Informal"
    correct_formal = 0
    correct_informal = 0
    false_formal = 0
    false_informal = 0
    for filename in os.listdir(path):
        if filename == ".DS_Store":
            continue
        file = path + "/" + filename
        #print file
        msg = ""
        for line in open(file, 'r'):
            msg = msg + " " + line
        featureset = f.extract_features(msg)
        predicted_label = classifier.classify(featureset)
        print filename,predicted_label #naivebayes object
        if predicted_label == "formal":
            if filename in formal:
                correct_formal += 1
                print "correct\n"
            else:
                false_formal += 1
                print "incorrect\n"

        else:
            if filename in informal:
                correct_informal += 1
                print "correct\n"
            else:
                false_informal += 1
                print "incorrect\n"

    accuracy = (float)(correct_formal + correct_informal) / (len(formal) + len(informal))
    print accuracy * 100, "%"
    print correct_formal,false_formal,correct_informal,false_informal


if __name__ == "__main__":
    main()