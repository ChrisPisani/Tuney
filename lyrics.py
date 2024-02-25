"""
Python class that cleans up song lyrics

"""

from collections import Counter
from collections import defaultdict
from collections import namedtuple
import string
from textblob import TextBlob
from lexicon import Lexicon

Clump = namedtuple('Clump', 'original filtered emotion')

class Lyrics:
    """
    Class for cleaning, and creating a dictionary of emotions for lyrics
    """
    def __init__(self):
        self.lexicon = Lexicon()

    def filter_lyrics(self, blob):
        """
        Given a blob of lyrics, filter out unncessary words
        """

        # a list of CLump namedtuples
        lyrics = []
        splitText = blob.split()
        for sentence in splitText:
            text = TextBlob(sentence)
            filtered = []

            # ignore any Genius tags
            # type pre process - word, post process - str
            if '[' not in sentence and sentence:
                for index, word in enumerate(text.words):
                    word = clean_word(word)

                    if not self.lexicon.is_stop_word(word):
                        # a window sliding algo that just checks if previous word is a negation
                        if index > 0 and "n't" in text.words[index - 1]:
                            filtered.append('nt-' + word)
                        else:
                            filtered.append(word)

                lyrics.append(Clump(original=sentence, filtered=filtered, emotion=defaultdict(int)))

        return lyrics

    def get_lyrics_emotions(self, lyrics):
        """
        Given filtered lyrics, return a dictionary of emotions that corresponds to each sentence

        """

        lyrics_emotions = []
        for clump in lyrics:
            if not len(clump.filtered) == 0:
                emotions = self.lexicon.word_association(clump.filtered)
                clump = Clump(original=clump.original, filtered=clump.filtered, emotion=emotions)
                lyrics_emotions.append(clump)

        return lyrics_emotions

def read_song_lyrics_from_file(songpath):
    """
    For testing purposes, reads lyrics from a file
    """
    lyrics = []

    with open(songpath, 'r') as file:
        for line in file:
            lyrics.append(line)

    return '\n'.join(lyrics)

def clean_word(word):
    """
    Cleans up the word and reduce it to its stem form.
    """

    word = word.lemmatize()
    word = word.lower()
    word = word.translate(str.maketrans('', '', string.punctuation))

    return word
