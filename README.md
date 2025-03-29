
# yt-audio-picker

A Python-based YouTube audio downloader that allows you to download and convert YouTube videos to MP3 format with a specified audio quality.

## Features

- Download audio from YouTube videos in MP3 format.
- Convert audio to your preferred bitrate (320 kbps, 256 kbps, 192 kbps, etc.).
- Supports custom download directories.
- Saves audio files with a timestamp in the filename to avoid conflicts.
- Optional thumbnail embedding and metadata processing.

## Requirements

- Python 3.x
- `yt-dlp` library (installable via pip)
- `FFmpeg` (used for audio conversion)

## Installation

1. Clone this repository or download the script.

2. Install the required Python dependencies:

   ```bash
   pip install yt-dlp
   ```

3. Install FFmpeg if you don't have it:

   - On Ubuntu/Debian:

     ```bash
     sudo apt install ffmpeg
     ```

   - On macOS:

     ```bash
     brew install ffmpeg
     ```

   - On Windows, download FFmpeg from the [official website](https://ffmpeg.org/download.html) and add it to your system's PATH.

## Usage

### Running the Script

To use the script, simply run the Python file:

```bash
python main.py
```

### Steps:

1. **Enter the YouTube video URL**: You'll be prompted to enter a valid YouTube URL from which you wish to download the audio.

2. **Select the download directory**: Optionally, specify a directory where the audio file will be saved (default is `downloads`).

3. **Select the audio quality**: Choose an audio quality from the available options (`320`, `256`, `192`, `128`, etc.). If no input is provided, the default quality is `320` kbps.

4. **Download Process**: The script will download the audio in the selected quality and save it as an MP3 file with a timestamp to avoid file name conflicts.

### Example:

```bash
yt-audio-picker
==================================================
Please enter YouTube video URL: https://www.youtube.com/watch?v=xyz123
Enter download directory (press Enter for default 'downloads'): my_music
Select audio quality in kbps (320/256/192/128/96/64) [default: 320]: 256
Downloading audio from: https://www.youtube.com/watch?v=xyz123
Found: Sample Video Title
Starting download with quality: 256kbps
Download complete! File saved to my_music
Download successful!
```

## Notes

- The script automatically creates the output directory if it does not exist.
- If you encounter any issues with the download, ensure that you have `FFmpeg` installed and properly configured.
- You can press `Ctrl + C` to cancel the download process at any time.

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENSE) file for details.
