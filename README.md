# Professional Music Player

A feature-rich music player built with Python and PyQt5.

## Features

- 🎵 Play, pause, and control music playback
- 📋 Playlist management with add/remove functionality
- 🎨 Display song information (title, artist, duration)
- ⏱️ Progress bar with seek functionality
- 🔄 Repeat and shuffle modes
- 💾 Save and load playlists (JSON format)
- 🖼️ Display album artwork
- 📥 Drag & drop support for music files
- 🌓 Dark/Light theme support
- ⌨️ Keyboard shortcuts

## Keyboard Shortcuts

- `Space`: Play/Pause
- `Left Arrow`: Previous song
- `Right Arrow`: Next song
- `Up Arrow`: Increase volume
- `Down Arrow`: Decrease volume

## Installation

### Using Setup Script (Recommended for Windows)
1. Run the setup script:
   ```bash
   setup.bat
   ```
   This will:
   - Create a virtual environment
   - Activate it
   - Install all required dependencies

### Manual Installation
1. Create a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment (if not already activated):
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

2. Run the music player:
   ```bash
   python music_player.py
   ```

3. Add music files:
   - Use the "File" menu to open individual files or folders
   - Drag and drop music files into the playlist
   - Supported formats: MP3, WAV, OGG

4. Control playback:
   - Use the control buttons or keyboard shortcuts
   - Adjust volume using the slider
   - Enable/disable repeat and shuffle modes
   - Search through your playlist using the search bar

5. Save/Load playlists:
   - Use the "File" menu to save or load playlists
   - Playlists are saved in JSON format

6. Change theme:
   - Use the "Theme" menu to switch between light and dark themes

## Requirements

- Python 3.7+
- PyQt5
- Mutagen
- Pygame

## License

This project is licensed under the MIT License - see the LICENSE file for details. 