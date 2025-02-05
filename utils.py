import json
import re
import string


# Listing stopwords is necessary for text cleaning (removing useless words)
STOPWORDS = set([
    "the", "a", "an", "is", "in", "on", "at", "for", "to", "with", "and", "or",
    "this", "that", "of", "by", "it", "its", "as", "was", "were", "be"
])


# Function whose main purpose is to extract IDs of documents, to use later in indexes
# Checks for errors

def extract_product_info(url):
    """
    Extracts product ID and variant from a given URL.
    """
    product_info = {"product_id": None, "variant": None}
    if not url:
        return product_info
    try:
        pattern = re.compile(r'/product/(\d+)(?:\?variant=([\w-]+))?')
        match = pattern.search(url)
        if match:
            product_info["product_id"] = match.group(1)
            product_info["variant"] = match.group(2) if match.group(2) else None
    except Exception as e:
        print(f"Error extracting product info: {e}")
    return product_info


# Function of tokenization of the text, 
# removing stopwords (cleaning the text) and converting to lowercase. Lemmatization is not implemented (not demanded). 

def preprocess_text(text):
    """
    Tokenizes text, removes punctuation and stopwords, and converts to lowercase.
    """
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    return [word for word in text.split() if word not in STOPWORDS]


# Function converting output sets to lists before creating the json files as outputs
# Checks for errors

def save_json(data, filename):
    """
    Saves dictionary data as JSON, converting sets to lists.
    """
    def convert_sets(obj):
        if isinstance(obj, set):
            return list(obj)  # Convert sets to lists
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=convert_sets)


# function for loading json files
# checks for errors

def load_json(filename):
    """
    Loads JSON file.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
