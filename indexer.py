import json
from collections import defaultdict
from utils import extract_product_info, preprocess_text, save_json

# The three Indexer classes are here clearly separated. Even if they have methods with similar names (build_index), this is polymorphism. Each method is
# adapted for the class it's used for. 

# First, the class ProductIndexer, which produces the inverted indexes for each token, one rendering the titles that contain it, and at which positions,
# the other rendering the descriptions that contain it and (similarly) at which positions.
# They are optimized so as to avoid duplications.

class ProductIndexer:
    def __init__(self):
        self.title_index = defaultdict(lambda: defaultdict(set))
        self.description_index = defaultdict(lambda: defaultdict(set))

    def index_product(self, product_id, title, description):
        """
        Indexes title and description while ensuring positions are not duplicated.
        """
        seen_positions = defaultdict(set)  # Prevent duplicate positions for the same word-product pair

        for pos, word in enumerate(preprocess_text(title)):
            if pos not in seen_positions[word]:  # Prevent duplicates
                self.title_index[word][product_id].add(pos)
                seen_positions[word].add(pos)

        seen_positions.clear()  # Reset for description

        for pos, word in enumerate(preprocess_text(description)):
            if pos not in seen_positions[word]:
                self.description_index[word][product_id].add(pos)
                seen_positions[word].add(pos)

    def build_index(self, file_path):
        """
        Reads JSONL file and builds the positional indexes.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line.strip())
                product_info = extract_product_info(data.get("url", ""))
                product_id = product_info["product_id"]

                if product_id:
                    self.index_product(product_id, data.get("title", ""), data.get("description", ""))

    def save_indexes(self):
        """
        Saves indexes to JSON files.
        """
        save_json(self.title_index, "data/title_index.json")
        save_json(self.description_index, "data/description_index.json")


# Second, the class ReviewIndexer that outputs for each document some basic information about its reviews : number of reviews, average score,
# and latest score. It ignores textual data (written reviews). An NLP model could analyze them, but this is beyond the scope of this work. 

class ReviewIndexer:
    def __init__(self):
        self.review_index = defaultdict(lambda: {"total_reviews": 0, "avg_rating": 0, "latest_rating": None})

    def index_reviews(self, product_id, reviews):
        """
        Indexes review statistics.
        """
        if not reviews:
            return
        total_reviews = len(reviews)
        ratings = [review["rating"] for review in reviews if isinstance(review.get("rating"), (int, float))]
        if ratings:
            avg_rating = sum(ratings) / total_reviews
            latest_rating = ratings[-1]
            self.review_index[product_id] = {
                "total_reviews": total_reviews,
                "avg_rating": round(avg_rating, 2),
                "latest_rating": latest_rating
            }

    def build_index(self, file_path):
        """
        Reads JSONL file and builds the review index.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line.strip())
                product_info = extract_product_info(data.get("url", ""))
                if product_info["product_id"]:
                    self.index_reviews(product_info["product_id"], data.get("product_reviews", []))

    def save_indexes(self):
        """
        Saves review index to JSON.
        """
        save_json(self.review_index, "data/review_index.json")


# Finally, the FeatureIndexer class, that 

class FeatureIndexer:
    def __init__(self):
        self.feature_index = defaultdict(lambda: defaultdict(set))

    def index_features(self, product_id, features):
        """
        Indexes features such as brand, origin, etc.
        """
        for key, value in features.items():
            if value:
                for word in preprocess_text(value):
                    self.feature_index[key][word].add(product_id)

    def build_index(self, file_path):
        """
        Reads JSONL file and indexes features.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line.strip())
                product_info = extract_product_info(data.get("url", ""))
                if product_info["product_id"]:
                    self.index_features(product_info["product_id"], data.get("product_features", {}))

    def save_indexes(self):
        """
        Saves feature indexes to JSON.
        """
        save_json(self.feature_index, "data/feature_index.json")
