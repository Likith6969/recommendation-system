import streamlit as st
import pandas as pd
import pickle
import requests
import random


def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=22f76699ebf28f10f1e07b1778ac29aa&language=en-US")
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    new_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in new_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


similarity = pickle.load(open("similarity.pkl", "rb"))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")


theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark"])
if theme == "Dark":
    bg_color = "#1e1e1e"
    text_color = "#ffffff"
    card_color = "#2c2c2c"
    header_color = "#FF9F1C"  # Dark orange for header visibility
else:
    bg_color = "#ffffff"
    text_color = "#000000"
    card_color = "#f0f0f0"
    header_color = "#FF4B4B"

# Movie title colors (cycled or random)
title_colors = ["#FF4B4B", "#1E90FF", "#32CD32", "#FFD700", "#FF69B4"]

# Custom CSS
st.markdown(f"""
    <style>
        .main {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .card {{
            transition: transform 0.2s;
        }}
        .card:hover {{
            transform: scale(1.05);
        }}
        h1 {{
            text-align: center;
            color: {header_color};
        }}
        p {{
            text-align: center;
            color: gray;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p>Pick a movie you like and get personalized recommendations!</p>", unsafe_allow_html=True)

# Movie selection
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            color = title_colors[idx % len(title_colors)]  # Cycle through colors
            st.markdown(f"""
            <div class='card' style='text-align:center; background-color:{card_color}; padding:10px; border-radius:10px; box-shadow: 2px 2px 15px rgba(0,0,0,0.2);'>
                <h4 style='color:{color}'>{names[idx]}</h4>
                <img src='{posters[idx]}' style='width:100%; border-radius:10px'>
            </div>
            """, unsafe_allow_html=True)





