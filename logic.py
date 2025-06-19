from difflib import get_close_matches
import nltk
from nltk.corpus import wordnet as wn
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from extra.finding_vectors import get_formality_axis

# Dummy dictionary (replace/expand as needed)
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
formality_axis = get_formality_axis()

# Suggestion logic
def get_suggestions(prefix):
    if not prefix:
        return []
    syns = get_synonyms(prefix)
    if not syns:
        raise Exception("no synonyms")
    candidates = [prefix] + syns
    embeddings = model.encode(candidates)
    scores = cosine_similarity(embeddings, [formality_axis]).flatten()
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1])  # lowest = least formal
    return ranked[:5]

# def edit_sentence(sentence, style):
#     if not isinstance(sentence, list):
#         raise TypeError("Input must be of type 'list'")
#     if not isinstance((word for word in sentence), str):
#         raise TypeError("Inputs must be strings")
#     revised = ''

#     return revised

# Synonym fetch function
def get_synonyms(word):
    print(word)
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ").lower()
            if name != word:
                synonyms.add(name)
    return list(synonyms)

# high_register_words = [
#     "pugilistic", "besotted", "filched", "querulous", "abet", "ignominious",
#     "effulgent", "perfidious", "cacophony", "obsequious", "vociferous",
#     "perspicacious", "vicissitude", "recalcitrant", "penurious", "lachrymose"
# ]

# simpler_synonyms = {}
# for word in high_register_words:
#     syns = get_synonyms(word)
#     if not syns:
#         continue
#     candidates = [word] + syns
#     embeddings = model.encode(candidates)
#     scores = cosine_similarity(embeddings, [formality_axis]).flatten()
#     ranked = sorted(zip(candidates, scores), key=lambda x: x[1])  # lowest = least formal
#     simpler_synonyms[word] = ranked[:5]  # top 5 simpler

# for word, alternatives in simpler_synonyms.items():
#     print(f"\n{word.upper()}:")
#     for alt, score in alternatives:
#         print(f"  {alt:20s} score={score:.3f}")


