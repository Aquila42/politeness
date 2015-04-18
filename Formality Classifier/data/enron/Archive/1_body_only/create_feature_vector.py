import glob

count=0

feature_vectors = open('feature_vectors_1','w')

# get all lines from trigrams_1_final and set count = 0
features = dict()
features_dict = open('trigrams_1_final')
features_dict_line = features_dict.readline()
while features_dict_line:
	features[features_dict_line] = 0
	features_dict_line = features_dict.readline()

features_dict = open('trigrams_0_final', 'w')
features_dict_line = features_dict.readline()
while features_dict_line:
	features[features_dict_line] = 0
	features_dict_line = features_dict.readline()

for filename in glob.glob('*.txt'):
	count = count + 1
	text = open(filename)
	text_body = text.read()
	for f in features:
		# if f exists in text_body: increment dictionary value


	string = ''
	for x in features:
		string = string + str(features[x]) + ' '
	# go through dictionary and add each element in one line e.g 0 0 1 2
	string = string + '\n'
	feature_vectors.write(string)

feature_vectors.close()
print count