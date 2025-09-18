import re
from collections import Counter
import nltk
from nltk import word_tokenize, pos_tag

# Safe download guards
for resource in ['punkt', 'averaged_perceptron_tagger']:
    try:
        nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'taggers/{resource}')
    except LookupError:
        nltk.download(resource)

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
