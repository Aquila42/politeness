import glob
import re
import nltk
from nltk import word_tokenize 
from nltk.util import ngrams

file_trigrams = open('trigrams_1','a')
count=0

# othernum = re.compile('[\d]*[,-:.][\d]+') # formatted numbers [e.g. dates, times]
# singnum = re.compile('[\d]+$') # individual numbers
# ordinal = re.compile('[\d]+[st|nd|rd|th]', re.I) # ordinal numbers


for filename in glob.glob('*.txt'):
	count = count + 1
	print count

	x = open(filename)
	text1 = x.read()

	# replace numbers with special character %NUM
	# re.sub(r'_u\d_v\d', '_u%d_v%d', inputtext)
	text2 = re.sub(r'[\d]+[st|nd|rd|th]', '__NUM__', text1)
	text2 = re.sub(r'[\d]*[,-:.][\d]+', '__NUM__', text2)
	text2 = re.sub(r'[\d]+', '__NUM__', text2)
	# print text2


	string = ''
	token_lower_case=nltk.word_tokenize(text2.lower())
	trigrams=ngrams(token_lower_case,3)
	for trigram in trigrams:
		string = string + str(trigram) + '\n'		


	file_trigrams.write(string)

	# if count==1: break

file_trigrams.close()