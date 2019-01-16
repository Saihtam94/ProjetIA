import nltk
import json

from collections import Counter

from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def parseBody(text):
	filtered_words = prepareText(text)

	data = dict()

	for word in filtered_words:
		# Count words in text.
		count(word, data)
	return data

def parseBodyStemming(text):
	filtered_words = prepareText(text)

	ps = PorterStemmer()
	data = dict()

	for word in filtered_words:
		# Stemming.
		word_stem = ps.stem(word)

		# Count words in text.
		count(word_stem, data)

	return data

def parseBodyLemmatization(text):
	filtered_words = prepareText(text)

	wnl = WordNetLemmatizer()
	data = dict()

	for word in filtered_words:
		# Lemmatization
		word_lem = wnl.lemmatize(word, get_pos(word))
		# Count words in text.
		count(word_lem, data)
	return data

def count(word, data):
	if word in data:
		data[word] = data[word]+1
	else:
		data[word] = 1

	#print(word + ' : ' + str(data[word]))

def get_pos(word):
    w_synsets = wordnet.synsets(word)

    pos_counts = Counter()
    pos_counts["n"] = len([item for item in w_synsets if item.pos()=="n"])
    pos_counts["v"] = len([item for item in w_synsets if item.pos()=="v"])
    pos_counts["a"] = len([item for item in w_synsets if item.pos()=="a"])
    pos_counts["r"] = len([item for item in w_synsets if item.pos()=="r"])

    most_common_pos_list = pos_counts.most_common(3)
    return most_common_pos_list[0][0] # first indexer for getting the top POS from list, second indexer for getting POS from tuple(POS: count)

def prepareText(initialText):
	# Remove punctuation.
	punctuations = '.,'
	text = ''

	for char in initialText:
		if char not in punctuations:
			text = text + char

	# Text in lowercase ?
	text = text.lower()

	# Tokenization.
	words = word_tokenize(text)

	# Remove stopwords.
	filtered_words = [word for word in words if word not in stopwords.words('english')]
	return filtered_words

def parser(d):
	return json.dumps(d)
