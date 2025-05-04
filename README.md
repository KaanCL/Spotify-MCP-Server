# Spotify MCP Server

A Model-Context-Protocol (MCP) server implementation for Spotify that enables AI assistants and other clients to control Spotify playback through a standardized protocol.

## What is MCP?

Model-Context-Protocol (MCP) is a framework that allows AI models and assistants to interact with external tools and services through a standardized interface. This project creates an MCP server that exposes Spotify functionality, making it accessible to any MCP-compatible client, including AI assistants.

## Features

* 🔍 **Search**: Search for songs on Spotify
* ▶️ **Play**: Play songs on your active Spotify device
* ⏸️ **Pause**: Pause currently playing music
* ⏭️ **Next Track**: Skip to the next track
* ⏮️ **Previous Track**: Go back to the previous track
* 🔊 **Volume Control**: Adjust the playback volume
* 👤 **User Info**: Get current user information
* 📋 **Playlists**: View your Spotify playlists
* 🎵 **Now Playing**: Get information about the currently playing track

## Prerequisites

* Python 3.11 or higher
* Spotify Premium account
* Spotify Developer credentials

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/spotify-mcp.git
   cd spotify-mcp
   ```

2. Set up a virtual environment:
   ```bash
   uv venv
   ```

3. Install dependencies:
   
   **Using UV (recommended for all dependencies):**
   ```bash
   uv sync
   ```
   
   **If you need to install Spotipy separately:**
   ```bash
   pip install spotipy
   ```
   Note: FastMCP will be installed through `uv sync` based on your project configuration.

## Configuration

1. Create a Spotify application at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Get your Client ID and Client Secret from your Spotify application
3. Create a `.env` file in the project root with your credentials:
   ```
   CLIENT_ID=your-spotify-client-id
   CLIENT_SECRET=your-spotify-client-secret
   REDIRECT_URI=http://localhost:8888/callback
   ```

## Initialization

When you run the MCP server for the first time:

1. A browser window will open asking you to log in to your Spotify account
2. You'll need to authorize the application to access your Spotify account
3. After authorization, you'll be redirected to the callback URL
4. The MCP server will initialize and start listening for connections on port 8080

## Usage

Run the MCP server:
```bash
python main.py
```

The server will initialize and register the following MCP tools that can be called by clients:

| Tool Name | Description | Parameters |
|----------|-------------|------------|
| `search` | Find songs on Spotify | `query: str` |
| `start_playback` | Play a specific song | `track_name: str` |
| `pause_playback` | Pause the currently playing song | None |
| `resume_playback` | Resume paused playback | None |
| `next_track` | Skip to the next track | None |
| `previous_track` | Go back to the previous track | None |
| `get_user_playlists` | View your Spotify playlists | None |
| `set_player_volume` | Adjust the volume | `volume: int` (0-100) |
| `current_playback` | Get information about what's playing | None |
| `get_current_user` | Get user profile information | None |

### MCP Client Example

Any MCP-compatible client can interact with this server, including AI assistants and programmatic clients:

```python
from mcp.client import MCPClient

# Connect to the MCP server
client = MCPClient("http://localhost:8080")

# Search for a song
results = client.call("search", {"query": "Money Tress"})

# Play a song
client.call("start_playback", {"track_name": "Money Tress"})

# Pause playback
client.call("pause_playback")
```

## How It Works: MCP Architecture

This project follows the Model-Context-Protocol architecture:

1. **MCP Server**: The core component that registers tools and handles requests
2. **FastMCP Implementation**: Uses the FastMCP library to create a lightweight, high-performance MCP server
3. **Spotify Integration**: Connects to the Spotify API using Spotipy
4. **Tool Registration**: Each Spotify function is registered as an MCP tool with appropriate type hints and documentation

The MCP server exposes these tools through a standardized protocol, allowing AI models and other clients to discover and call the tools without needing to understand the underlying Spotify API implementation details.

## Security Notes

* Your Spotify credentials are stored locally in the `.env` file
* The `.env` file is excluded from git through the `.gitignore` file
* The MCP server only accepts connections from localhost by default
* Always keep your credentials secure and never commit them to version control
