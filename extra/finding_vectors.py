import os
import joblib
import numpy as np
import nltk
from nltk.corpus import wordnet as wn
from sentence_transformers import SentenceTransformer

# Download WordNet resources
nltk.download('wordnet')
nltk.download('omw-1.4')

# Path to project root (2 levels up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Define where to save the file
FORMALITY_AXIS_PATH = os.path.join(CACHE_DIR, "formality_axis.pkl")

# Load model (not cached, loaded fresh each time)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Your formality axis construction (just an example)
def get_formality_axis_unused():
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
    formal_vec = np.mean(model.encode(formal_words), axis=0)
    informal_vec = np.mean(model.encode(informal_words), axis=0)
    return formal_vec - informal_vec

# Your formality axis construction (just an example)
def get_formality_axis():
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
                "notify", "predict", "subsequently", "furthermore", "moreover", "consequently", "hence", "thus", "notwithstanding", "albeit", "whereas", "thereby", "heretofore", "hereinafter"]
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
 "start", "keep up", "let know", "guess", "later", "plus", "also", "so", "therefor", "like", "but", "by doing that", "before that", "after that"]
    formal_vec = np.mean(model.encode(formal_words), axis=0)
    informal_vec = np.mean(model.encode(informal_words), axis=0)
    return formal_vec - informal_vec



# Save the axis if needed
if not os.path.exists(FORMALITY_AXIS_PATH):
    formality_axis = get_formality_axis()
    joblib.dump(formality_axis, FORMALITY_AXIS_PATH)


