import streamlit as st
import pandas as pd
import requests
import pickle
import gdown
import os

# -------------------------------
# 📦 Download + Load Data (Cached)
# -------------------------------

FILE_ID = "1irOOl0YQysxsR41e0MvjOsfH52Aw2U5T"
FILE_PATH = "movie_data.pkl"

@st.cache_data(show_spinner=True)
def load_data():
    # Download file if not present
    if not os.path.exists(FILE_PATH):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, FILE_PATH, quiet=False, fuzzy=True)

    # Load pickle file
    with open(FILE_PATH, "rb") as f:
        movies, cosine_sim = pickle.load(f)

    return movies, cosine_sim

movies, cosine_sim = load_data()

# -------------------------------
# 🎯 Recommendation Function
# -------------------------------

def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# -------------------------------
# 🎬 Fetch Poster from TMDB
# -------------------------------

def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]  # 🔐 secure key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/150"
    
    except:
        return "https://via.placeholder.com/150"

# -------------------------------
# 🖥️ Streamlit UI
# -------------------------------

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.subheader("Top 10 Recommended Movies:")

    # 2 rows × 5 columns layout
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
