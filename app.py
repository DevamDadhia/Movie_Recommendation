import streamlit as st
import pandas as pd
import requests
import pickle
import os

# -------------------------------
# CONFIG
# -------------------------------
FILE_PATH = "movie_data.pkl"
FILE_URL = "https://huggingface.co/datasets/devv123/movie-recommender-data/resolve/main/movie_data.pkl"

# -------------------------------
# DOWNLOAD FILE (FINAL STABLE)
# -------------------------------
def download_file():
    response = requests.get(FILE_URL, stream=True)
    
    if response.status_code != 200:
        raise Exception("Download failed")

    with open(FILE_PATH, "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    if not os.path.exists(FILE_PATH):
        st.info("Downloading data... please wait ⏳")
        try:
            download_file()
        except Exception:
            st.error("❌ Download failed from Hugging Face")
            st.stop()

    # File validation
    file_size = os.path.getsize(FILE_PATH)

    if file_size < 100_000_000:
        st.error("❌ File corrupted or incomplete download")
        st.stop()

    st.success(f"✅ Data loaded ({file_size / (1024*1024):.2f} MB)")

    try:
        with open(FILE_PATH, "rb") as f:
            movies, cosine_sim = pickle.load(f)
    except Exception:
        st.error("❌ Failed to load .pkl file")
        st.stop()

    return movies, cosine_sim


movies, cosine_sim = load_data()

# -------------------------------
# RECOMMENDATION
# -------------------------------
def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# -------------------------------
# POSTER FETCH
# -------------------------------
def fetch_poster(movie_id):
    try:
        api_key = st.secrets["TMDB_API_KEY"]
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        data = requests.get(url).json()
        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/150"
    except:
        return "https://via.placeholder.com/150"

# -------------------------------
# UI
# -------------------------------
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie)
    st.subheader("Top 10 Recommended Movies")

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
