import pickle
import streamlit as st
import pandas as pd
import requests

# Set the page title and icon
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bca760832242f445b873908aa955c216&language=en-US"
    try:
        response = requests.get(url)
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to fetch the movie rating
def fetch_rating(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bca760832242f445b873908aa955c216&language=en-US"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('vote_average', 'N/A')  # Return 'N/A' if rating is not available
    except requests.exceptions.RequestException:
        return 'N/A'

# Function to recommend movies
def recommend(movie, genre=None):
    if movie not in movies['title'].values:
        return ["Movie not found"], ["https://via.placeholder.com/500x750?text=No+Image"], ["N/A"]
    
    movie_index = movies[movies['title'] == movie].index[0]
    movie_list = sorted(enumerate(similarity[movie_index]), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movie_posters = []
    recommended_movie_ratings = []
    
    for i in movie_list[1:16]:
        movie_id = movies.iloc[i[0]].movie_id # Ensure 'movie_id' column exists
        movie_title = movies.iloc[i[0]].title # Ensure 'title' column exists
        movie_genres = new_movie.iloc[i[0]].genres  #  Ensure 'genres' column exists
        
        
        # Filter by genre if specified and genre is not "Not Selected"
        if genre and genre != "Not Selected" and genre not in movie_genres:
            continue  # Skip this movie if it doesn't match the selected genre
        
        # Fetch poster and rating
        poster = fetch_poster(movie_id)
        rating = fetch_rating(movie_id)  
        
        # Append the movie details to the lists
        recommended_movies.append(movie_title)
        recommended_movie_posters.append(poster)
        recommended_movie_ratings.append(rating)
    
    return recommended_movies, recommended_movie_posters, recommended_movie_ratings

# Load the movie dictionary which contains the movie titles and IDs
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

# Create a DataFrame from the dictionary
movies = pd.DataFrame(movies_dict)
# Load the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Load the new_movie DataFrame which contains the movie genres , ratings and other details
new_movie = pickle.load(open('new.pkl', 'rb'))

st.header('Movie Recommendation System')

# Create a dropdown list of movies
selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values,
)

# create a sidebar for genre selection 
st.sidebar.title("🎭 Explore by Genre")
# Create a dropdown list of genres in the sidebar
genre = st.sidebar.selectbox("Select Genre", ["Not Selected", "Action", "Comedy", "Drama", "Sci-Fi"])


# Create a button to show recommendations
if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        # Pass the selected genre to the recommend function
        recommended_movie_names, recommended_movie_posters, recommended_movie_ratings = recommend(selected_movie_name, genre if genre != "Not Selected" else None) # Pass None if genre is "Not Selected"
    
    # cols = st.columns(5)
    # for i in range(len(recommended_movie_names)):
    #     with cols[i]:
    #         st.image(recommended_movie_posters[i], use_column_width=True)
    #         st.write(f"**{recommended_movie_names[i]}**")
    #         st.write(f"⭐ Rating: {recommended_movie_ratings[i]}/10")
    if recommended_movie_names:
        num_movies = len(recommended_movie_names)
        cols = st.columns(num_movies)  # Create only as many columns as needed

        for i in range(num_movies):
            with cols[i]:  
                st.image(recommended_movie_posters[i], use_container_width=True)  
                st.write(f"**{recommended_movie_names[i]}**")  
                st.write(f"⭐ Rating: {recommended_movie_ratings[i]}/10")
else:
    st.warning("No movies found matching your selection. Try a different genre or movie!")