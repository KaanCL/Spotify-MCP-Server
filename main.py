
from mcp.server.fastmcp import FastMCP
import spotify

mcp = FastMCP("SpotifyMCP")



@mcp.tool()
def search(query:str)->str:
    """Search for a song on Spotify"""
    result = spotify.search(query)
    return result

@mcp.tool()
def start_playback(track_name: str) -> str:
    """Play a song on Spotify"""
    return spotify.start_playback(track_name)

@mcp.tool()
def get_current_user() -> str:
    """Get current user information"""
    result = spotify.get_current_user()
    return f"Current User: {result}"

@mcp.tool()
def pause_playback() -> str:
    """Pause the current playback"""
    return spotify.pause_playback()

@mcp.tool()
def resume_playback() -> str:
    """Resume the current playback"""
    return spotify.resume_playback()

@mcp.tool()
def next_track() -> str:
    """Skip to the next track"""
    return spotify.next_track()

@mcp.tool()
def previous_track() -> str:
    """Go back to the previous track"""
    return spotify.previous_track()

@mcp.tool()
def get_user_playlists() -> str:
    """Get user's playlists"""
    results = spotify.get_user_playlists()
    return str(results)

@mcp.tool()
def set_player_volume(volume: int) -> str:
    """Set the volume (0-100)"""
    return spotify.set_volume(volume)

@mcp.tool()
def current_playback() -> str:
    """Get information about what's currently playing"""
    return str(spotify.get_current_playback())