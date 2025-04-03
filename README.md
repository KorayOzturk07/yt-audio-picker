# YouTube Video & Audio Downloader (ytad.py)

## Description
`ytad.py` is a Python script for downloading both video and audio from YouTube. It uses `yt-dlp`, a powerful tool for extracting and downloading media from various online platforms. This script simplifies the process of downloading content in high-quality formats.

## Features
- Download audio or video from YouTube.
- Supports various formats and resolutions.
- Easy-to-use command-line interface.
- English and Turkish language support.

## Requirements
Ensure you have the following dependencies installed before running the script:

- Python 3.x
- `yt-dlp` (Install using `pip install yt-dlp`)
- `ffmpeg` (Required for processing media files, install via package manager)

## Installation
1. Clone the repository or download `ytad.py`:
   ```sh
   git clone https://github.com/yourusername/ytad.git
   cd ytad
   ```

2. Install required dependencies:
   ```sh
   pip install yt-dlp
   ```

3. Ensure `ffmpeg` is installed:
   ```sh
   sudo apt install ffmpeg   # For Debian/Ubuntu
   brew install ffmpeg       # For macOS
   choco install ffmpeg      # For Windows (Using Chocolatey)
   ```

## Usage
Before running the script, ensure you have `ytad.py` in your working directory.
Run the script from the command line with the YouTube video URL and specify whether you want to download audio or video:

### Download Audio
```sh
python ytad.py --audio <video_url>
```

Example:
```sh
python ytad.py --audio https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Download Video
```sh
python ytad.py --video <video_url>
```

Example:
```sh
python ytad.py --video https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## License
This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

## Contributing
Feel free to submit issues or pull requests to improve the script.

## Contact
For any questions or suggestions, contact [Koray Öztürk](https://github.com/KorayOzturk07)

