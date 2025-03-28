yt-audio-picker

A simple terminal-based YouTube audio downloader that extracts high-quality audio from YouTube videos and saves them as MP3 files.

Features

✅ Download highest quality audio from YouTube videos
✅ Saves audio as high-bitrate MP3 files
✅ Simple terminal-based user input
✅ Windows batch file (.bat) for easy execution

Requirements

Python 3.x installed

yt-dlp (YouTube downloader library)

ffmpeg (for audio conversion)

Installation

Install Python (if not already installed):

Download and install Python from: https://www.python.org/downloads/

Make sure to check the box "Add Python to PATH" during installation.

Install dependencies:
Open a terminal or command prompt and run:

pip install yt-dlp

You may also need ffmpeg:

sudo apt install ffmpeg  # Linux (Ubuntu/Debian)
choco install ffmpeg      # Windows (Chocolatey)
brew install ffmpeg       # macOS (Homebrew)

Usage

1. Run the Python script manually

Open a terminal or command prompt and run:

python main.py

Then, enter a YouTube video URL when prompted.

2. Use the Windows batch file (for easy execution)

If you're on Windows, simply double-click download_audio.bat to run the script.

Output Location

The downloaded MP3 files will be saved in the downloads/ folder inside the script directory.

Troubleshooting

Python not recognized? Ensure Python is added to your system PATH.

yt-dlp not found? Run pip install yt-dlp again.

ffmpeg errors? Ensure ffmpeg is installed and accessible from the command line.