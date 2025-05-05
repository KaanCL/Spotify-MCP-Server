from mcp.server.fastmcp import FastMCP
import spotify

# 🚀 Initialize the FastMCP server for Spotify integration
# -------------------------------------------------------
# This instance acts as the entry point for all Spotify-related tools.
# The FastMCP framework allows you to easily expose Python functions as API endpoints or tools.
# Here, we name our MCP instance "SpotifyMCP" for clarity and identification.
mcp = FastMCP("SpotifyMCP")

# ------------------------------------------------------------------------
# TOOL DEFINITIONS
# Each function below is decorated with @mcp.tool(), making it accessible
# as a tool in the MCP ecosystem. All tools are designed to interact with
# the Spotify API via the 'spotify' module and return results as dictionaries
# for seamless JSON serialization and API responses.
# ------------------------------------------------------------------------

@mcp.tool()
def search(query: str) -> dict:
    """
    🔍 Search for tracks on Spotify by query string.

    Args:
        query (str): The search term (track name, artist, album, etc.)

    Returns:
        dict: Search results including matching tracks, artists, and albums.

    Usage:
        Use this tool to find tracks or artists by keyword.
    """
    return spotify.search(query)

@mcp.tool()
def start_playback(track_name: str) -> dict:
    """
    ▶️ Start playback for a given track name.

    Args:
        track_name (str): The name of the track to play.

    Returns:
        dict: Playback status and metadata.

    Usage:
        Initiate playback of a specific track by providing its name.
    """
    return spotify.start_playback(track_name)

@mcp.tool()
def get_current_user() -> dict:
    """
    👤 Get the current Spotify user's profile information.

    Returns:
        dict: User profile details such as username, email, and subscription status.

    Usage:
        Retrieve information about the authenticated Spotify user.
    """
    return spotify.get_current_user()

@mcp.tool()
def pause_playback() -> dict:
    """
    ⏸️ Pause the current playback.

    Returns:
        dict: Playback status after pausing.

    Usage:
        Temporarily stop the current track without losing position.
    """
    return spotify.pause_playback()

@mcp.tool()
def resume_playback() -> dict:
    """
    ▶️ Resume playback if paused.

    Returns:
        dict: Playback status after resuming.

    Usage:
        Continue playback from where it was paused.
    """
    return spotify.resume_playback()

@mcp.tool()
def next_track() -> dict:
    """
    ⏭️ Skip to the next track.

    Returns:
        dict: Playback status and information about the new track.

    Usage:
        Move to the next track in the current playlist or queue.
    """
    return spotify.next_track()

@mcp.tool()
def previous_track() -> dict:
    """
    ⏮️ Return to the previous track.

    Returns:
        dict: Playback status and information about the previous track.

    Usage:
        Go back to the previous track in the playlist or queue.
    """
    return spotify.previous_track()

@mcp.tool()
def get_user_playlists() -> dict:
    """
    📋 Retrieve the user's playlists.

    Returns:
        dict: A list of playlists owned or followed by the user.

    Usage:
        Fetch all playlists associated with the current user account.
    """
    return spotify.get_user_playlists()

@mcp.tool()
def set_player_volume(volume: int) -> dict:
    """
    🔊 Set the Spotify player's volume (0-100).

    Args:
        volume (int): Desired volume level (must be between 0 and 100).

    Returns:
        dict: Status of the volume change operation.

    Usage:
        Adjust the playback volume for the current Spotify session.
    """
    return spotify.set_volume(volume)

@mcp.tool()
def current_playback() -> dict:
    """
    🎵 Get info about the currently playing track.

    Returns:
        dict: Details about the current playback, including track, artist, and playback state.

    Usage:
        Retrieve real-time information about what is currently playing.
    """
    return spotify.get_current_playback()

# =============================================================================
# 🛠️ Developer Notes:
# -----------------------------------------------------------------------------
# - All MCP tools are designed to return Python dictionaries for easy JSON
#   serialization and integration with web APIs or front-end clients.
# - To extend functionality, simply add new @mcp.tool() functions following
#   the same pattern as above.
# - For debugging or logging, you can print or log responses within each tool.
# - Type hints and detailed docstrings are provided for all tools to enhance
#   code clarity, maintainability, and discoverability (especially in IDEs).
# - Ensure that the 'spotify' module implements the required API interactions.
# - For authentication and authorization, make sure the Spotify API credentials
#   are properly configured in your environment.
# =============================================================================