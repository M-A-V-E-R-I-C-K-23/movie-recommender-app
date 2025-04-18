import streamlit as st
import pandas as pd
import pickle
import requests

def movie_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=14a28bbe51139037bdb77720e4e3f694&language=en-US')
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"  # fallback image
    except:
        return "https://via.placeholder.com/500x750?text=Error"


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_genre = pickle.load(open('genre_map.pkl', 'rb'))

st.title('🎬 Movie Recommender System')

selected_Movie_Name = st.selectbox('Which Movie Would You like To Search?', movies['title'].values)
selected_Genre = st.selectbox('Or select a Genre to explore movies:', ['None'] + sorted(movie_genre.keys()))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movies_List = similarity[movie_index]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_List:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(movie_poster(movie_id))

    return recommended_movies, recommended_movies_poster

def recommend_by_genre(genre):
    recommended_movies = []
    recommended_movies_poster = []

    if genre in movie_genre:
        movie_indices = movie_genre[genre][:5]  # just showing first 5 for simplicity
        for idx in movie_indices:
            movie_id = movies.iloc[idx].movie_id
            recommended_movies.append(movies.iloc[idx].title)
            recommended_movies_poster.append(movie_poster(movie_id))
    return recommended_movies, recommended_movies_poster

if st.button('Search'):
    if selected_Genre != 'None':
        movie_names, movie_posters = recommend_by_genre(selected_Genre)
    else:
        movie_names, movie_posters = recommend(selected_Movie_Name)

    cols_per_row = 5
    for idx, (name, poster) in enumerate(zip(movie_names, movie_posters)):
        if idx % cols_per_row == 0:
            cols = st.columns(cols_per_row)
        with cols[idx % cols_per_row]:
            st.text(name)
            st.image(poster)