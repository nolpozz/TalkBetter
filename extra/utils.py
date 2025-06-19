# utils.py
import os

def get_cache_path(filename):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cache"))
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, filename)
