"""
Lexicon module
"""

from nltk.corpus import stopwords
from nrclex import NRCLex
import pandas as pd

BAD_WORD_FILEPATH = 'lexicon/bad-words.txt'

class Lexicon:
    """
    Class for all things related to a lexicon (stop words, NRC lexicon, etc)
    """
    def __init__(self):
        columns = ['word', 'emotion', 'association']

        self.curse = pd.read_fwf(BAD_WORD_FILEPATH, names=['word'], skiprows=1)

        self.stop_words = set(stopwords.words('english'))

        # words left over from lemmatize
        self.stop_words.add('ai') # ain't
        self.stop_words.add('wa') # wasn't
        self.stop_words.add('ca') # can't
        self.stop_words.add('wo') # won't
        self.stop_words.add('nt')
        self.stop_words.add('m')

    def word_association(self, word):

        # Iterate through list
        if word[0]:
            emotion = NRCLex(word[0])
        return emotion.raw_emotion_scores

    def is_stop_word(self, word):
        """
        Checks if the word is a stop_word
        """

        if (word.isdigit() or word in self.stop_words or (self.curse['word'] == word).any()):
            return True

        return False
