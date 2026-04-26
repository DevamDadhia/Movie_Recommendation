import streamlit as st
import pandas as pd
import requests
import pickle
import gdown
import os

# -------------------------------
# 📦 CONFIG
# -------------------------------
FILE_ID = "1irOOl0YQysxsR41e0MvjOsfH52Aw2U5T"
FILE_PATH = "movie_data.pkl"

# -------------------------------
# 📥 DOWNLOAD + LOAD DATA
# -------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    if not os.path.exists(FILE_PATH):
        st.info("📥 Downloading data... Please wait (first run only)")
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, FILE_PATH, quiet=False, fuzzy=True)

    try:
        with open(FILE_PATH, "rb") as f:
            movies, cosine_sim = pickle.load(f)
    except Exception as e:
        st.error("❌ Failed to load data file. Please check Google Drive link.")
        st.stop()

    return movies, cosine_sim

movies, cosine_sim = load_data()

# -------------------------------
# 🎯 RECOMMENDATION FUNCTION
# -------------------------------
def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# -------------------------------
# 🎬 FETCH POSTER
# -------------------------------
def fetch_poster(movie_id):
    try:
        api_key = st.secrets["TMDB_API_KEY"]
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        response = requests.get(url)
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/150"

    except:
        return "https://via.placeholder.com/150"

# -------------------------------
# 🖥️ UI
# -------------------------------
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie)
    st.subheader("Top 10 Recommended Movies:")

    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)

                with col:
                    st.image(poster_url, width=130)
                    st.caption(movie_title)
