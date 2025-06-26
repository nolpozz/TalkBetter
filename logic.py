from difflib import get_close_matches
import nltk
from nltk.corpus import wordnet as wn
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import joblib
import matplotlib.pyplot as plt


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
    if prefix is None:
        return ["waiting"]
    syns = get_synonyms(prefix)
    if not syns:
        return []
    candidates = [] + syns
    embeddings = model.encode(candidates)
    scores = cosine_similarity(embeddings, [formality_axis]).flatten()
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1])  # lowest = least formal
    return ranked[:5]

def get_word_score(word):
    if word is None:
        return None
    embedding = model.encode(word)
    score = cosine_similarity([embedding], [formality_axis]).flatten()
    return float(score)


def display_formality_axis():
    test_words = [
    "commence", "initiate", "begin", "start", "kick off",
    "utilize", "employ", "use", "grab", "snag",
    "subsequently", "afterward", "then", "later", "next",
    "notwithstanding", "however", "but", "though", "still"
]
    test_embeddings = model.encode(test_words)
    test_scores = cosine_similarity(test_embeddings, [formality_axis]).flatten()
    
    plt.figure(figsize=(12, 8))
    plt.scatter(range(len(test_words)), test_scores)

    for i, word in enumerate(test_words):
        plt.annotate(word, (i, test_scores[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.axhline(y=0, color='r', linestyle='--')

    plt.xlabel("Word Index")
    plt.ylabel("Formality Score")
    plt.title("Formality Scores of Test Words")
    plt.grid(True)
    plt.show()