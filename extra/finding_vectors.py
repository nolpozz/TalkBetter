import nltk
from nltk.corpus import wordnet as wn
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Download WordNet resources
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Your high-register word list
high_register_words = [
    "pugilistic", "besotted", "filched", "querulous", "abet", "ignominious",
    "effulgent", "perfidious", "cacophony", "obsequious", "vociferous",
    "perspicacious", "vicissitude", "recalcitrant", "penurious", "lachrymose"
]

# Formality axis construction
formal_words = ["assist", "reside", "depart", "arrive", "permit", 
                "acquire", "consume", "investigate", "respond", 
                "disclose", "construct", "reject", "delay", "commence", 
                "purchase", "inform", "endeavor", "request", "cease", 
                "encounter", "repair", "demonstrate", "conclude", 
                "eliminate", "verify", "decrease", "postpone", "occupy", 
                "utilize", "authorize", "commence", "contain", "establish", 
                "facilitate", "illustrate", "indicate", "operate", "retain", 
                "appear", "ascertain", "consult", "prohibit", "discontinue", 
                "observe", "function", "implement", "initiate", "maintain", 
                "notify", "predict"]
informal_words = ["help", "live", "leave", "show up", "let", 
 "get", "eat", "look into", "reply", "tell", 
 "build", "turndown", "hold off", "start", 
 "buy", "tell", "try", "ask for", "stop", 
 "meet", "fix", "show", "finish", 
 "get rid of", "check", "cut down", 
 "put off", "take up", "use", "okay", "kick off", 
 "hold", "set up", "help", "show", "point out", 
 "run", "keep", "show up", "find out", "ask", 
 "ban", "quit", "see", "work", "carry out", 
 "start", "keep up", "let know", "guess"]

def get_formality_axis():
    formal_vec = np.mean(model.encode(formal_words), axis=0)
    informal_vec = np.mean(model.encode(informal_words), axis=0)
    formality_axis = formal_vec - informal_vec
    return formality_axis

formal_vec = np.mean(model.encode(formal_words), axis=0)
informal_vec = np.mean(model.encode(informal_words), axis=0)
formality_axis = formal_vec - informal_vec

# # Synonym fetch function
def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ").lower()
            if name != word:
                synonyms.add(name)
    return list(synonyms)

# Score synonyms by formality
simpler_synonyms = {}
for word in high_register_words:
    syns = get_synonyms(word)
    if not syns:
        continue
    candidates = [word] + syns
    embeddings = model.encode(candidates)
    scores = cosine_similarity(embeddings, [formality_axis]).flatten()
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1])  # lowest = least formal
    simpler_synonyms[word] = ranked[:5]  # top 5 simpler

# Print results
for word, alternatives in simpler_synonyms.items():
    print(f"\n{word.upper()}:")
    for alt, score in alternatives:
        print(f"  {alt:20s} score={score:.3f}")
