Movie Recommendation System 🎬


The Movie Recommendation System is a Python-based web application that helps users discover movies similar to their favorite ones. Built using Streamlit, Pandas, and Pickle, this system utilizes a similarity matrix to recommend movies based on content similarity. Additionally, users can filter recommendations by genre for a more personalized experience.


🔹 Key Features:

✔️ Movie Similarity-Based Recommendations – Suggests movies based on content similarity.

✔️ Genre Filtering – Users can filter recommendations by selecting a specific genre.

✔️ Poster Fetching – Displays movie posters using the TMDb API.

✔️ Movie Ratings – Fetches and shows ratings for each recommended movie.

✔️ Interactive UI – Built with Streamlit for an easy-to-use experience.


🛠️ Technologies Used:

Python 🐍

Streamlit 🎨 (For the web interface)

Pandas 📊 (For data processing)

Pickle 📦 (For storing similarity matrices)

TMDb API 🎥 (For fetching posters and ratings)



📂 Data Used:

movie_dict.pkl – Stores movie IDs and titles.

new.pkl – Contains detailed movie data (genre, cast, etc.).

similarity.pkl – Precomputed similarity matrix for recommendations.



💡 Future Improvements:


🔹 Implement collaborative filtering for better recommendations.

🔹 Add sorting options (popularity, release year, etc.).

🔹 Enhance UI with animations and user profiles.



📂 File Structure

📁 movie-recommender
│── t.py              # Main Streamlit app


│── new.pkl             # Processed movie dataset


│── movie_dict.pkl      # Movie dictionary
|

│── similarity.pkl      # Similarity matrix
|

│── README.md           # Project documentation



📊 Dataset & Preprocessing


Movies are loaded from movie_dict.pkl and new.pkl.

A TF-IDF similarity matrix is loaded from similarity.pkl.

Genre filtering is applied to show relevant movies.



📜 License

This project is open-source and available under the MIT License.



🚀 Future Improvements


🔹 Implement collaborative filtering for better recommendations.

🔹 Improve recommendation accuracy with deep learning.

🔹 Add more filtering options like language and year.



Developer :
Sumit Kumar Jaiswal 
email : sumit500123@gmail.com 
