import pandas as pd
import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "aa91168e8a3b4121a9911de878ad4ed7"
CLIENT_SECRET = "478fa5f79f334792988c9ec6f4b13e3e"

# Initialize the Spotify client
client_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"  # Update the search query format
    results = sp.search(q=search_query, type="track")

    print("Search query:", search_query)  # Add this line to check the search query

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print("Album cover URL:", album_cover_url)  # Check the album cover URL
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = df[df['track_name'] == song].index[0]
    distances = sorted(list(enumerate(similar[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        track_artist = df.iloc[i[0]].track_artist
        print(track_artist)
        print(df.iloc[i[0]].track_name)
        recommended_music_posters.append(get_song_album_cover_url(df.iloc[i[0]].track_name, track_artist))
        recommended_music_names.append(df.iloc[i[0]].track_name)

    return recommended_music_names,recommended_music_posters



st.image('Spotify.png',width = 600)
st.markdown("<h1 style = 'color: #000000; text-align: center;font-family: Arial, Helvetica, sans-serif; '>'Music Recommendation System'</h1>", unsafe_allow_html= True)
st.markdown("<h3 style = 'margin: -25px; color: #000000; text-align: center;font-family: Arial, Helvetica, sans-serif; '> Created by Ayodeji</h3>", unsafe_allow_html= True)

df = pd.read_pickle("df.pkl") 
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 2000)
vectors = cv.fit_transform(df['tags']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similar = cosine_similarity(vectors)

music_list = df['track_name'].values
select_music = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_songs,recommended_song_covers = recommend(select_music)
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.text(recommended_songs[0])
        st.image(recommended_song_covers[0])
    with col2:
        st.text(recommended_songs[1])
        st.image(recommended_song_covers[1])

    with col3:
        st.text(recommended_songs[2])
        st.image(recommended_song_covers[2])
    with col4:
        st.text(recommended_songs[3])
        st.image(recommended_song_covers[3])
    with col5:
        st.text(recommended_songs[4])
        st.image(recommended_song_covers[4])