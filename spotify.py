import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Replace with your Spotify API credentials
CLIENT_ID = 'a3a291840977445780e81b8e345f81c2'
CLIENT_SECRET = '97859f53b1a24a5dbbe43477296af573'
REDIRECT_URI = 'http://localhost:8888/callback'
# Updated scopes to include additional endpoints
SCOPE = (
    'user-top-read user-library-read playlist-read-private '
    'user-read-recently-played user-read-playback-state '
    'user-read-currently-playing user-follow-read'
)

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


def get_top_medium(limit=50, time_range='medium_term'):
    top_tracks = sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)
    answer = []
    for idx, item in enumerate(top_tracks['items'], 1):
        track = item['name']
        artist = item['artists'][0]['name']
        answer.append(f"{idx}. {track} - {artist}")
    if answer == []: return ["None"]
    return answer

def get_top_short(limit=50, time_range='short_term'):
    top_tracks = sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)
    answer = []
    for idx, item in enumerate(top_tracks['items'], 1):
        track = item['name']
        artist = item['artists'][0]['name']
        answer.append(f"{idx}. {track} - {artist}")
    if answer == []: return ["None"]
    return answer

def get_top_long(limit=50, time_range='long_term'):
    top_tracks = sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)
    answer = []
    for idx, item in enumerate(top_tracks['items'], 1):
        track = item['name']
        artist = item['artists'][0]['name']
        answer.append(f"{idx}. {track} - {artist}")
    if answer == []: return ["None"]
    return answer

def get_top_artists_medium(limit=50, time_range='medium_term'):
    top_artists = sp.current_user_top_artists(limit=limit, offset=0, time_range=time_range)
    answer = []
    for idx, item in enumerate(top_artists['items'], 1):
        answer.append(f"{idx}. {item['name']}")
    if answer == []: return ["None"]
    return answer

def get_top_artists_short(limit=50, time_range='short_term'):
    top_artists = sp.current_user_top_artists(limit=limit, offset=0, time_range=time_range)
    answer = []
    for idx, item in enumerate(top_artists['items'], 1):
        answer.append(f"{idx}. {item['name']}")
    if answer == []: return ["None"]
    return answer

def get_top_artists_long(limit=50, time_range='long_term'):
    top_artists = sp.current_user_top_artists(limit=limit, offset=0, time_range=time_range)
    answer = []
    for idx, item in enumerate(top_artists['items'], 1):
        answer.append(f"{idx}. {item['name']}")
    if answer == []: return ["None"]
    return answer

def get_saved_tracks(limit=50):
    saved_tracks = sp.current_user_saved_tracks(limit=limit)
    answer = []
    for idx, item in enumerate(saved_tracks['items'], 1):
        track = item['track']['name']
        artist = item['track']['artists'][0]['name']
        answer.append(f"{idx}. {track} - {artist}")
    if answer == []: return ["None"]
    return answer

def get_recently_played(limit=50):
    recently_played = sp.current_user_recently_played(limit=limit)
    answer = []
    for idx, item in enumerate(recently_played['items'], 1):
        track = item['track']['name']
        artist = item['track']['artists'][0]['name']
        played_at = item['played_at']
        answer.append(f"{idx}. {track} - {artist} at {played_at}")
    if answer == []: return ["None"]
    return answer

def get_followed_artists(limit=20):
    followed = sp.current_user_followed_artists(limit=limit)
    answer = []
    # The followed artists are nested under 'artists'
    for idx, item in enumerate(followed['artists']['items'], 1):
        answer.append(f"{idx}. {item['name']}")
    if answer == []: return ["None"]
    return answer

def get_saved_albums(limit=20):
    saved_albums = sp.current_user_saved_albums(limit=limit)
    answer = []
    for idx, item in enumerate(saved_albums['items'], 1):
        album = item['album']
        artists = ", ".join(artist['name'] for artist in album['artists'])
        answer.append(f"{idx}. {album['name']} by {artists}")
    if answer == []: return ["None"]
    return answer

def main():
    # Build a dictionary with all the results
    data = {
        "top tracks over a few months": get_top_medium(),
        "top tracks over many years": get_top_long(),
        "top tracks over a few weeks": get_top_short(),
        "top artists over a few months": get_top_artists_medium(),
        "top artists over many years": get_top_artists_long(),
        "top artists over a few weeks": get_top_artists_short(),
        "saved tracks": get_saved_tracks(),
        "recently played": get_recently_played(),
        "followed artists": get_followed_artists(),
        "saved albums": get_saved_albums()
    }
    
    # Print the entire result as formatted JSON
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
