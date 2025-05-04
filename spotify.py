import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

SCOPE = "user-read-private user-read-email user-library-read user-read-playback-state user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


def search(query):
    results = sp.search(q=query, limit=5, type='track')
    tracks = []
    for item in results["tracks"]["items"]:
        track = {
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "uri": item["uri"],
            "url": item["external_urls"]["spotify"]
        }
        tracks.append(track)
    return tracks
   


def start_playback(track):
    results = sp.search(q=track, limit=1, type='track')
    if not results["tracks"]["items"]:
        return "No tracks found"
        
    track_uri = results['tracks']['items'][0]['uri']
    sp.start_playback(uris=[track_uri])
    
    return f"Playing {results['tracks']['items'][0]['name']} by {results['tracks']['items'][0]['artists'][0]['name']}"


def get_current_user():
    user_info = sp.current_user()
    return {
        "display_name": user_info.get("display_name"),
        "email": user_info.get("email"),
        "id": user_info.get("id")
    }


def pause_playback():
    sp.pause_playback()
    return "Playback paused"

def resume_playback():
    sp.start_playback()
    return "Playback resumed"


def next_track():
    sp.next_track()
    return "Skipped to next track"

def previous_track():
    sp.previous_track()
    return "Returned to previous track"



def get_user_playlists():
    playlists = sp.current_user_playlists()
    result = []
    
    for playlist in playlists['items']:
        playlist_info = {
            "name": playlist['name'],
            "url": playlist['external_urls']['spotify'],
            "id": playlist['id'],
            "tracks_total": playlist['tracks']['total']
        }
        result.append(playlist_info)
        
    return result


def set_volume(volume):
    if not isinstance(volume, int) or volume < 0 or volume > 100:
        return "Volume must be an integer between 0 and 100"
            
    sp.volume(volume)
    return f"Volume set to {volume}"


def get_current_playback():
    playback = sp.current_playback()
    if playback is None:
        return "Nothing is playing"
    
    track = playback['item']
    result = {
        "is_playing": playback['is_playing'],
        "track_name": track['name'],
        "artist": track['artists'][0]['name'],
        "album": track['album']['name'],
        "progress_ms": playback['progress_ms'],
        "duration_ms": track['duration_ms']
    }
    
    return result

