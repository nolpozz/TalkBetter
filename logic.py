from difflib import get_close_matches
import nltk
from nltk.corpus import wordnet as wn
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from extra.finding_vectors import get_formality_axis
import os
import joblib


# Dummy dictionary (replace/expand as needed)
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
FORMALITY_AXIS_PATH = os.path.join(PROJECT_ROOT, "cache", "formality_axis.pkl")

# Load the cached formality axis
formality_axis = joblib.load(FORMALITY_AXIS_PATH)

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
    if not word:
        return ["waiting"]
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ").lower()
            if name != word:
                synonyms.add(name)
    return list(synonyms)

# Suggestion logic
def get_suggestions(prefix):
    syns = get_synonyms(prefix)
    if not syns:
        return []
        # raise Exception("no synonyms")
    candidates = [prefix] + syns
    embeddings = model.encode(candidates)
    scores = cosine_similarity(embeddings, [formality_axis]).flatten()
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1])  # lowest = least formal
    return ranked[:5]
