from indexer import ProductIndexer, FeatureIndexer, ReviewIndexer


# This class is the entry point of the program. 

# You can execute it in VSCODE or with bash "Indexation_Web_TP2_YoucefBoulfrad/python3 main.py"


def main():
    file_path = "data/products.jsonl"

    # Build and save title/description index
    product_indexer = ProductIndexer()
    product_indexer.build_index(file_path)
    product_indexer.save_indexes()

    # Build and save feature index
    feature_indexer = FeatureIndexer()
    feature_indexer.build_index(file_path)
    feature_indexer.save_indexes()

    # Build and save review index
    review_indexer = ReviewIndexer()
    review_indexer.build_index(file_path)
    review_indexer.save_indexes()

    print("All indexes have been built and saved successfully.")

if __name__ == "__main__":
    main()
