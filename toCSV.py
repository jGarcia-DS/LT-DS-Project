import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# API Credentials
cid = 'ec57adf8e193493fb88daa14a7c29a09'
secret = 'c731cf768c074e0c9e7270b579b5520e'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager= client_credentials_manager)

# Playlist to dataframe
def call_playlist(creator, playlist_id):
    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    results = sp.user_playlist_tracks(creator,playlist_id)

    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for track in tracks:
        playlist_features = {}
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]

        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]

        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index=[0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)

    return playlist_df

# ID to find playlist

ID = input('Enter ID ')
name = input('Enter File Name ')+'.csv'
playlist = call_playlist('spotify',ID).to_csv('/Users/jaggergarcia/PycharmProjects/SpotifyComp/PlaylistData/'+name)


