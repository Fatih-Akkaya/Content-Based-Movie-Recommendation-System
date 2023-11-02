import streamlit as st
import pandas as pd
import pickle
import os
import base64
import random

path_to_dataset = r"models/movie_list.pkl"
path_to_model = r"models/model.pkl"

# Modeli yükle
with open(path_to_model, 'rb') as model_file:
    tfidf_vectorizer = pickle.load(model_file)
    similarity = pickle.load(model_file)

movies = pd.read_pickle(path_to_dataset)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    .block-container {{
        background-color: rgb(38 38 38 / 80%);
        min-height: -webkit-fill-available;

    }}
    .stMarkdown h1,  .stMarkdown p {{
        color: rgb(255 255 255 / 80%);
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('images/2012-movie-collage31-2048x1448.jpg')

def get_recommendations(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:10]:
        recommended_movie_posters.append(f'https://image.tmdb.org/t/p/w500{movies.loc[index, "poster_path"]}')
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def display_recommendations(recommendations):
    for idx, (_, row) in enumerate(recommendations.iterrows()):
        artist = row['artist_name']
        track = row['track_name']
        album = row['album_name']
        cover_image_url = row['album_image_url']
        spotify_url = row['track_uri'].replace("/track/", "/embed/track/")

        col1, col2 = st.columns([0.75, 1])

        with col1:
            st.image(cover_image_url, width=150)
            st.write(f"**Sanatçı:** {artist}")
            st.write(f"**Şarkı:** {track}")
            st.write(f"**Albüm:** {album}")

        with col2:
            st.write(
                f'<iframe src="{spotify_url}" width="350" height="180" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>',
                unsafe_allow_html=True
            )

        if idx < len(recommendations) - 1:
            st.markdown("✂➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")


def create_playlist_from_artists(artists):
    song_indices = []
    for artist in artists:
        artist_songs_df = df[df['artist_name'] == artist]
        if len(artist_songs_df) <= 3:
            song_indices.extend(artist_songs_df.index.tolist())
        else:
            song_indices.extend(artist_songs_df.sample(3).index.tolist())

    return df.loc[song_indices]


st.title('Movie Recommendation System')
with st.container():
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list)

    if st.button('List Recommendations'):
        recommended_movie_names,recommended_movie_posters = get_recommendations(selected_movie)
        recommended_movie_list = [(key, value) for (key, value) in zip(recommended_movie_names,recommended_movie_posters)]
        groups = []
        n = 3
        for i in range(0, len(recommended_movie_list), n):
            groups.append(recommended_movie_list[i:i+n])

        for group in groups:
            cols = st.columns(n)
            for i, (movie_name, movie_poster) in enumerate(group):
                with cols[i]:
                    st.image(movie_poster, width=150)
                    st.write(f'*** {movie_name} ***')

