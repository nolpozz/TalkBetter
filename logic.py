from difflib import get_close_matches

# Dummy dictionary (replace/expand as needed)
DICTIONARY = ['hello', 'help', 'helicopter', 'her', 'hero', 'heritage', 'hey', 'high', 'how', 'house']

# Suggestion logic
def get_suggestions(prefix):
    if not prefix:
        return []
    return get_close_matches(prefix, DICTIONARY, n=5, cutoff=0.3)


def edit_sentence(sentence):
    if not isinstance(sentence, list):
        raise TypeError("Input must be of type 'list'")
    if not isinstance((word for word in sentence), str):
        raise TypeError("Inputs must be strings")
    pass

