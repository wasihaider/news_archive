from nltk.corpus import stopwords
from stemmer import Stemmer
import re, string

#############################################

class Preprocessor:

	def __init__(self):
		self.stopwords = set(stopwords.words('english'))
		self.stemmer = Stemmer()

	#########################################

	def remove_stop_words(self, document):
		altered = re.sub(r'[^\x00-\x7F]+', ' ', document)
		altered = re.sub(r'@\w+', '', altered)
		altered = altered.lower()
		altered = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', altered)
		altered = re.sub(r'[0-9]', '', altered)
		altered = re.sub(r'\s{2,}', ' ', altered)
		altered = altered.split(' ')

		clean_words = []
		for word in altered:
			if word not in self.stopwords:
				clean_words.append(word)

		return clean_words

	#########################################

	def stem_words(self, words):
		stemmed_words = []
		for word in words:
			if not word.isalpha() and word:
				stemmed_words.append(
						self.stemmer.stem(word, 0, len(word)-1)
					)
			else:
				stemmed_words.append(word)

		return stemmed_words

	#########################################

	def get_preprocessed_words(self, document):
		middle_state = self.remove_stop_words(document)
		final_words = self.stem_words(middle_state)

		return final_words


#############################################