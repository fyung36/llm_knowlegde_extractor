import re
from collections import Counter
import nltk
from nltk import word_tokenize, pos_tag

# Safe download guards
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

def extract_top_nouns(text: str, top_n: int = 3):
    if not text or len(text.strip()) < 5:
        return []

    tokens = word_tokenize(text.lower())
    tagged = pos_tag(tokens)
    nouns = [word for word, pos in tagged if pos.startswith("NN") and word.isalpha()]

    if not nouns:
        return []

    most_common = Counter(nouns).most_common(top_n)
    return [word for word, _ in most_common]
