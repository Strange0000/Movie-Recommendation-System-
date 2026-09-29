import os
import pickle
import streamlit as st
import pandas as pd
import requests
from pathlib import Path

# Set the page title and icon
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")


# --- Auto-generate similarity.pkl if missing or invalid ---
def generate_similarity_matrix():
    """Generate similarity.pkl from movie tags if it doesn't exist."""
    similarity_path = Path("similarity.pkl")

    # Check if similarity.pkl exists and is valid (not an LFS pointer)
    needs_generation = False
    if not similarity_path.exists():
        needs_generation = True
    elif similarity_path.stat().st_size < 1000:
        # LFS pointer files are ~134 bytes; real file is ~176 MB
        needs_generation = True

    if needs_generation:
        with st.spinner("🔧 First-time setup: Building similarity matrix (this takes ~10 seconds)..."):
            from sklearn.feature_extraction.text import CountVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            with open("movie_dict.pkl", "rb") as f:
                movies_dict = pickle.load(f)

            movies_df = pd.DataFrame(movies_dict)
            movies_df["tags"] = movies_df["tags"].fillna("")

            cv = CountVectorizer(max_features=5000, stop_words="english")
            vectors = cv.fit_transform(movies_df["tags"])
            sim = cosine_similarity(vectors)

            with open("similarity.pkl", "wb") as f:
                pickle.dump(sim, f)

        st.success("✅ Similarity matrix built successfully!")


# Run auto-generation before loading data
generate_similarity_matrix()


# --- TMDB API Key ---
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "bca760832242f445b873908aa955c216")


# --- Data Loading (cached) ---
@st.cache_data
def load_movies():
    with open("movie_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)
    return pd.DataFrame(movies_dict)


@st.cache_data
def load_similarity():
    with open("similarity.pkl", "rb") as f:
        return pickle.load(f)


@st.cache_data
def load_new_movie():
    with open("new.pkl", "rb") as f:
        return pickle.load(f)


@st.cache_data
def get_all_genres(_new_movie_df):
    """Extract all unique genres from the dataset."""
    all_genres = set()
    for genres in _new_movie_df["genres"]:
        if isinstance(genres, list):
            all_genres.update(genres)
    return sorted(all_genres)


# --- API Functions ---
def fetch_movie_details(movie_id):
    """Fetch poster and rating in a single API call."""
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={TMDB_API_KEY}&language=en-US"
    )
    placeholder_poster = "https://via.placeholder.com/500x750?text=No+Image"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        poster = (
            f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
            if data.get("poster_path")
            else placeholder_poster
        )
        rating = data.get("vote_average", "N/A")
        return poster, rating
    except requests.exceptions.RequestException:
        return placeholder_poster, "N/A"


# --- Recommendation Function ---
def recommend(movie, genre=None):
    """Recommend movies based on similarity, optionally filtered by genre."""
    if movie not in movies["title"].values:
        return [], [], []

    movie_index = movies[movies["title"] == movie].index[0]
    movie_list = sorted(
        enumerate(similarity[movie_index]), reverse=True, key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_movie_posters = []
    recommended_movie_ratings = []

    for i in movie_list[1:50]:  # Check more candidates to fill after genre filtering
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title
        movie_genres = new_movie.iloc[i[0]].genres

        # Filter by genre if specified
        if genre and genre != "Not Selected" and genre not in movie_genres:
            continue  # Skip if genre doesn't match

        # Fetch poster and rating in one call
        poster, rating = fetch_movie_details(movie_id)

        recommended_movies.append(movie_title)
        recommended_movie_posters.append(poster)
        recommended_movie_ratings.append(rating)

        # Stop after 10 recommendations
        if len(recommended_movies) >= 10:
            break

    return recommended_movies, recommended_movie_posters, recommended_movie_ratings


# --- Load Data ---
movies = load_movies()
similarity = load_similarity()
new_movie = load_new_movie()

# --- UI ---
st.header("🎬 Movie Recommendation System")

# Movie selection dropdown
selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies["title"].values,
)

# Sidebar: Genre filter with dynamic genre list
st.sidebar.title("🎭 Explore by Genre")
all_genres = get_all_genres(new_movie)
genre = st.sidebar.selectbox("Select Genre", ["Not Selected"] + all_genres)

# Show recommendations on button click
if st.button("Show Recommendation"):
    with st.spinner("Fetching recommendations..."):
        recommended_movie_names, recommended_movie_posters, recommended_movie_ratings = (
            recommend(selected_movie_name, genre if genre != "Not Selected" else None)
        )

    if recommended_movie_names:
        num_movies = len(recommended_movie_names)
        # Display in rows of 5
        for row_start in range(0, num_movies, 5):
            row_end = min(row_start + 5, num_movies)
            cols = st.columns(row_end - row_start)
            for idx, col in enumerate(cols):
                i = row_start + idx
                with col:
                    st.image(recommended_movie_posters[i], use_container_width=True)
                    st.write(f"**{recommended_movie_names[i]}**")
                    st.write(f"⭐ Rating: {recommended_movie_ratings[i]}/10")
    else:
        st.warning(
            "No movies found matching your selection. Try a different genre or movie!"
        )