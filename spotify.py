import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth
from enum import Enum
from typing import List, Dict, Any, Optional, Union

# 🌱 Load environment variables from .env file for secure credential management
# --------------------------------------------------------------------------------
# The following line loads environment variables from a .env file into the process's
# environment. This is a best practice for managing sensitive credentials such as
# API keys, client secrets, and redirect URIs, as it keeps them out of the source code.
# --------------------------------------------------------------------------------
load_dotenv()

# --------------------------------------------------------------------------------
# Retrieve Spotify API credentials and redirect URI from environment variables.
# These variables must be set in the .env file or the system environment for the
# authentication process to work correctly.
# --------------------------------------------------------------------------------
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

class SpotifyScope(Enum):
    """
    Enum for Spotify API scopes.

    Scopes define the level of access the application has to a user's Spotify account.
    Each scope enables specific API endpoints, such as reading user data, controlling
    playback, or accessing playlists. For more information, refer to the Spotify API
    documentation: https://developer.spotify.com/documentation/general/guides/authorization/scopes/
    """
    USER_READ_PRIVATE = "user-read-private"  # Access user's subscription details and country
    USER_READ_EMAIL = "user-read-email"      # Access user's email address
    USER_LIBRARY_READ = "user-library-read"  # Access user's saved tracks and albums
    USER_READ_PLAYBACK_STATE = "user-read-playback-state"  # Read playback state
    USER_MODIFY_PLAYBACK_STATE = "user-modify-playback-state"  # Control playback

class SpotifyError(Enum):
    """
    Enum for error types.

    This enumeration standardizes error messages throughout the codebase, making it
    easier to handle and localize errors. Each error type corresponds to a specific
    failure scenario that may occur during Spotify API interactions.
    """
    NO_ACTIVE_DEVICE = "No active device found"  # No device is currently active for playback
    NO_TRACKS_FOUND = "No tracks found"          # No tracks matched the search query
    NOTHING_PLAYING = "Nothing is playing"       # No track is currently playing
    INVALID_VOLUME = "Volume must be an integer between 0 and 100"  # Volume out of range
    AUTH_ERROR = "Authentication error"          # Issues with authentication or authorization
    UNKNOWN = "Unknown error"                    # Any other unspecified error

def format_error(message: str, error_type: SpotifyError = SpotifyError.UNKNOWN) -> Dict[str, str]:
    """
    Standardized error formatting.

    Args:
        message (str): The error message to be displayed to the user.
        error_type (SpotifyError, optional): The type of error encountered. Defaults to UNKNOWN.

    Returns:
        dict: A dictionary containing a single key 'error' with a descriptive error message.
    
    This function ensures that all errors returned by the API have a consistent structure,
    making it easier for clients to handle and display errors.
    """
    return {"error": f"{error_type.value}: {message}"}

def ensure_active_device(sp: spotipy.Spotify) -> Optional[Dict[str, str]]:
    """
    Check if there is an active device for playback.

    Args:
        sp (spotipy.Spotify): An authenticated Spotipy client instance.

    Returns:
        dict | None: Returns an error dict if no active device is found, otherwise None.

    This utility function checks whether the user has an active Spotify device (such as
    a phone, desktop app, or web player) available for playback. Many Spotify API playback
    endpoints require an active device. If no device is found, an error is returned.
    """
    devices = sp.devices()
    if not devices.get("devices"):
        return format_error("Please open Spotify on a device and try again.", SpotifyError.NO_ACTIVE_DEVICE)
    return None

# 🎧 Define the required Spotify API scopes for playback and user info
# --------------------------------------------------------------------------------
# The SCOPE variable is a space-separated string of all required permissions for this
# application. It is passed to the SpotifyOAuth object to request the necessary access
# from the user during authentication.
# --------------------------------------------------------------------------------
SCOPE = " ".join([
    SpotifyScope.USER_READ_PRIVATE.value,
    SpotifyScope.USER_READ_EMAIL.value,
    SpotifyScope.USER_LIBRARY_READ.value,
    SpotifyScope.USER_READ_PLAYBACK_STATE.value,
    SpotifyScope.USER_MODIFY_PLAYBACK_STATE.value,
])

# 🚀 Initialize the Spotipy client with OAuth authentication
# --------------------------------------------------------------------------------
# The Spotipy client is initialized with OAuth authentication, using the credentials
# and scopes defined above. This client is used for all subsequent Spotify API calls.
# --------------------------------------------------------------------------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def search(query: str) -> Union[List[Dict[str, Any]], Dict[str, str]]:
    """
    🔍 Search for tracks on Spotify.

    Args:
        query (str): The search query (song name, artist, etc.)

    Returns:
        list[dict] | dict: List of track info dicts, or error dict.

    This function performs a search for tracks on Spotify using the provided query.
    It returns up to 5 matching tracks, each represented as a dictionary containing
    the track's name, artist, album, URI, and Spotify URL. If no tracks are found,
    or if an error occurs, a standardized error dictionary is returned.
    """
    try:
        results = sp.search(q=query, limit=5, type='track')
        tracks = []
        for item in results["tracks"]["items"]:
            # 🎼 Collect essential track info for each result
            track = {
                "name": item["name"],
                "artist": item["artists"][0]["name"],
                "album": item["album"]["name"],
                "uri": item["uri"],
                "url": item["external_urls"]["spotify"]
            }
            tracks.append(track)
        if not tracks:
            return format_error("No tracks found for your query.", SpotifyError.NO_TRACKS_FOUND)
        return tracks
    except Exception as e:
        return format_error(str(e))

def start_playback(track: str) -> Dict[str, Any]:
    """
    ▶️ Start playback for a given track name.

    Args:
        track (str): Track name or search query.

    Returns:
        dict: Playback status or error.

    This function searches for the specified track and starts playback on the user's
    active Spotify device. If no device is active, or if the track is not found, an
    error is returned. On success, it returns the status and details of the playing track.
    """
    try:
        device_error = ensure_active_device(sp)
        if device_error:
            return device_error
        results = sp.search(q=track, limit=1, type='track')
        if not results["tracks"]["items"]:
            return format_error("No tracks found for playback.", SpotifyError.NO_TRACKS_FOUND)
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        return {
            "status": "playing",
            "track": results['tracks']['items'][0]['name'],
            "artist": results['tracks']['items'][0]['artists'][0]['name']
        }
    except spotipy.SpotifyException as e:
        return format_error(str(e), SpotifyError.AUTH_ERROR)
    except Exception as e:
        return format_error(str(e))

def get_current_user() -> Dict[str, Any]:
    """
    👤 Fetch the current Spotify user's profile.

    Returns:
        dict: User info or error.

    This function retrieves the profile information of the currently authenticated
    Spotify user, including their display name, email, and user ID. If authentication
    fails, an error is returned.
    """
    try:
        user_info = sp.current_user()
        return {
            "display_name": user_info.get("display_name"),
            "email": user_info.get("email"),
            "id": user_info.get("id")
        }
    except Exception as e:
        return format_error(str(e), SpotifyError.AUTH_ERROR)

def pause_playback() -> Dict[str, str]:
    """
    ⏸️ Pause the current playback.

    Returns:
        dict: Pause status or error.

    This function pauses the current playback on the user's active device. If no device
    is active, or if an error occurs, a standardized error is returned.
    """
    try:
        device_error = ensure_active_device(sp)
        if device_error:
            return device_error
        sp.pause_playback()
        return {"status": "paused"}
    except Exception as e:
        return format_error(str(e))

def resume_playback() -> Dict[str, str]:
    """
    ▶️ Resume playback if paused.

    Returns:
        dict: Resume status or error.

    This function resumes playback on the user's active device if it is currently paused.
    If no device is active, or if an error occurs, a standardized error is returned.
    """
    try:
        device_error = ensure_active_device(sp)
        if device_error:
            return device_error
        sp.start_playback()
        return {"status": "resumed"}
    except Exception as e:
        return format_error(str(e))

def next_track() -> Dict[str, str]:
    """
    ⏭️ Skip to the next track.

    Returns:
        dict: Skip status or error.

    This function skips to the next track in the user's playback queue on the active
    device. If no device is active, or if an error occurs, a standardized error is returned.
    """
    try:
        device_error = ensure_active_device(sp)
        if device_error:
            return device_error
        sp.next_track()
        return {"status": "skipped to next"}
    except Exception as e:
        return format_error(str(e))

def previous_track() -> Dict[str, str]:
    """
    ⏮️ Return to the previous track.

    Returns:
        dict: Previous status or error.

    This function returns to the previous track in the user's playback queue on the
    active device. If no device is active, or if an error occurs, a standardized error is returned.
    """
    try:
        device_error = ensure_active_device(sp)
        if device_error:
            return device_error
        sp.previous_track()
        return {"status": "returned to previous"}
    except Exception as e:
        return format_error(str(e))

def get_user_playlists() -> Union[List[Dict[str, Any]], Dict[str, str]]:
    """
    📋 Retrieve the user's playlists.

    Returns:
        list[dict] | dict: List of playlists or error.

    This function fetches all playlists owned or followed by the current user. Each
    playlist is represented as a dictionary containing its name, Spotify URL, ID, and
    the total number of tracks. If no playlists are found, or if an error occurs, a
    standardized error is returned.
    """
    try:
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
        if not result:
            return format_error("No playlists found.")
        return result
    except Exception as e:
        return format_error(str(e))

def set_volume(volume: int) -> Dict[str, str]:
    """
    🔊 Set the Spotify player's volume.

    Args:
        volume (int): Volume level (0-100).

    Returns:
        dict: Volume status or error.

    This function sets the playback volume on the user's active device. The volume must
    be an integer between 0 and 100. If the value is out of range, or if no device is
    active, a standardized error is returned.
    """
    if not isinstance(volume, int) or volume < 0 or volume > 100:
        return format_error("Volume must be an integer between 0 and 100", SpotifyError.INVALID_VOLUME)
    try:
        device_error = ensure_active_device(sp)
        if device_error:
            return device_error
        sp.volume(volume)
        return {"status": f"Volume set to {volume}"}
    except Exception as e:
        return format_error(str(e))

def get_current_playback() -> Dict[str, Any]:
    """
    🎵 Get info about the currently playing track.

    Returns:
        dict: Playback info or error.

    This function retrieves information about the currently playing track, including
    whether playback is active, the track's name, artist, album, progress in milliseconds,
    and total duration. If nothing is playing, or if an error occurs, a standardized
    error is returned.
    """
    try:
        playback = sp.current_playback()
        if playback is None or playback.get('item') is None:
            return format_error("Nothing is playing.", SpotifyError.NOTHING_PLAYING)
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
    except Exception as e:
        return format_error(str(e))

# 🛠️ Developer Notes:
# --------------------------------------------------------------------------------
# - All functions return either a dict or a list of dicts for easy JSON serialization.
# - Error handling is consistent; always check for an "error" key in the response.
# - For advanced use, consider adding logging or metrics here.
# - Enum types and utility functions are used for maintainability and clarity.
# - This module is designed to be imported and used by a web server or other backend
#   service that needs to interact with the Spotify API on behalf of a user.
# - For more information on the Spotify Web API, see:
#   https://developer.spotify.com/documentation/web-api/
# --------------------------------------------------------------------------------

