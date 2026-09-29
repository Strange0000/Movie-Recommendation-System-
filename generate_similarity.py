"""
Generate similarity.pkl from movie_dict.pkl

This script loads the movie tags from movie_dict.pkl,
computes cosine similarity using CountVectorizer, and
saves the result as similarity.pkl.
"""

import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def main():
    # Load movie dictionary
    print("Loading movie_dict.pkl...")
    with open("movie_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)

    movies = pd.DataFrame(movies_dict)
    print(f"Loaded {len(movies)} movies.")
    print(f"Columns: {movies.columns.tolist()}")

    # Ensure 'tags' column exists
    if "tags" not in movies.columns:
        raise ValueError("movie_dict.pkl does not contain a 'tags' column.")

    # Fill any NaN tags with empty string
    movies["tags"] = movies["tags"].fillna("")

    # Vectorize the tags using CountVectorizer
    print("Vectorizing tags with CountVectorizer (max_features=5000)...")
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(movies["tags"])
    print(f"Vectors shape: {vectors.shape}")

    # Compute cosine similarity
    print("Computing cosine similarity matrix...")
    similarity = cosine_similarity(vectors)
    print(f"Similarity matrix shape: {similarity.shape}")

    # Save to pickle
    output_file = "similarity.pkl"
    print(f"Saving to {output_file}...")
    with open(output_file, "wb") as f:
        pickle.dump(similarity, f)

    print(f"Done! File size: {__import__('os').path.getsize(output_file) / (1024*1024):.1f} MB")


if __name__ == "__main__":
    main()
