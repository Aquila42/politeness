__author__ = 'Aquila'
from subprocess import call
import os.path

#Separates the formal and informal mails


formal_path = "/Users/AQ/politeness/Formality Classifier/data/enron/sw_informal"

f1 = open(formal_path,"r")

for filename in f1:
    old_file = "/Users/AQ/politeness/Formality Classifier/data/enron/all_mails/"+filename.strip()+"_a.txt"
    if os.path.isfile(old_file):
        print ""
    else:
        old_file = "/Users/AQ/politeness/Formality Classifier/data/enron/all_mails/"+filename.strip()+"_b.txt"
        if os.path.isfile(old_file):
            print ""
        else:
            print filename
    new_file = "/Users/AQ/politeness/Formality Classifier/data/enron/informal/"+filename.strip()+".txt"
    call(["mv",old_file,new_file])
