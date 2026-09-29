# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built with **Python** and **Streamlit**. It suggests similar movies using cosine similarity on movie tags, displays posters and ratings via the TMDb API, and lets users filter by genre.

> 🌐 **Live Demo**: [movierecommender-st.streamlit.app](https://movierecommender-st.streamlit.app/)

---

## ✨ Key Features

- **Content-Based Recommendations** — Suggests movies based on cosine similarity of tags (overview, genres, keywords, cast, crew)
- **Genre Filtering** — Filter recommendations by any of 20 genres (Action, Comedy, Drama, Thriller, Sci-Fi, etc.)
- **Movie Posters & Ratings** — Fetches posters and ratings from the [TMDb API](https://www.themoviedb.org/)
- **Cached Data Loading** — Uses `@st.cache_data` for fast reruns
- **Responsive Layout** — Displays up to 10 recommendations in rows of 5

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 🐍 | Core language |
| Streamlit 🎨 | Web interface |
| Pandas 📊 | Data processing |
| Scikit-learn 🤖 | CountVectorizer + Cosine Similarity |
| TMDb API 🎥 | Movie posters & ratings |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Strange0000/Movie-Recommendation-System-.git
cd Movie-Recommendation-System-

# Install dependencies
pip install -r requirements.txt

# Generate the similarity matrix (first time only, takes ~10 seconds)
python generate_similarity.py

# Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501**.

---

## 📂 Project Structure

```
Movie-Recommendation-System-/
├── app.py                   # Main Streamlit app
├── generate_similarity.py   # Script to build similarity matrix
├── movie_dict.pkl           # Movie IDs, titles, and tags (4,806 movies)
├── new.pkl                  # Detailed movie data (genres, cast, crew, etc.)
├── similarity.pkl           # Generated cosine similarity matrix (not in repo)
├── t.py                     # Legacy app (original version)
├── restro.ipynb             # Data preprocessing notebook
├── requirements.txt         # Python dependencies
├── .gitignore               # Excludes similarity.pkl (176 MB)
└── README.md                # This file
```

> **Note**: `similarity.pkl` is not included in the repo (176 MB). Run `python generate_similarity.py` to create it locally.

---

## 📊 How It Works

1. **Data Preprocessing** — Movie metadata (overview, genres, keywords, cast, crew) is combined into a single `tags` field per movie
2. **Vectorization** — Tags are vectorized using `CountVectorizer` (5,000 features)
3. **Similarity** — Cosine similarity is computed between all 4,806 movies
4. **Recommendation** — When a user selects a movie, the top similar movies are retrieved and optionally filtered by genre
5. **Display** — Posters and ratings are fetched from TMDb and displayed in a grid

---

## 💡 Future Improvements

- 🔹 Implement collaborative filtering for better recommendations
- 🔹 Add sorting options (popularity, release year, etc.)
- 🔹 Add more filtering options like language and year
- 🔹 Enhance UI with animations and user profiles
- 🔹 Improve recommendation accuracy with deep learning

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Developer

**Sumit Kumar Jaiswal**
📧 sumit500123@gmail.com
