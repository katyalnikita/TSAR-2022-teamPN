import difflib
from spacy.lang.en import English
import spacy
import pattern
from pattern.en import pluralize, singularize

class SM(difflib.SequenceMatcher):
    def __init__(self, a):
        super().__init__(a=a)

    def __call__(self, b):
        self.set_seq2(b)
        return self.ratio()


nlp = English()
nlp = spacy.load('en_core_web_trf')


class NlpUtils:
    def __init__(self):
        print("")

    def get_pos(self, utterance, word):
        words = utterance.split(" ")
        water = SM(word)
        best = max(words, key=water)
        doc = nlp(utterance)
        for token in doc:
            if token.text == best or token.text == word:
                return token.pos_
    def get_noun_quantity(self,noun):
        if pluralize(noun) == noun:
            return "plural"
        if singularize(noun) == noun:
            return "singular"
    def set_noun_quantity(self,noun,quantity):
        if quantity == "singular":
            return singularize(noun)
        if quantity == "plural":
            return pluralize(noun)
        return noun



s = NlpUtils()
print(s.get_pos("John killed Mary with a gun.", "gun"))
print(s.get_noun_quantity("childs"))
