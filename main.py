import yt_dlp
import os
import sys
from datetime import datetime

def download_audio(url, output_dir="downloads", quality="320"):
    """
    Download audio from YouTube URL and convert to MP3
    
    Args:
        url (str): YouTube video URL
        output_dir (str): Directory to save downloaded files
        quality (str): Audio quality in kbps (320, 256, 192, 128, etc.)
    
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        
        # Add timestamp to avoid filename conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_template = os.path.join(output_dir, f'%(title)s_{timestamp}.%(ext)s')
        
        # Configure download options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'outtmpl': output_template,
            'noplaylist': True,  # Fixed typo in 'noplaylist'
            'quiet': False,
            'verbose': False,
            'progress': True,
            'writethumbnail': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                },
                {
                    'key': 'EmbedThumbnail',
                },
                {
                    'key': 'FFmpegMetadata',
                },
            ],
        }
        
        # Perform the download
        print(f"Downloading audio from: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown Title')
            print(f"Found: {video_title}")
            print(f"Starting download with quality: {quality}kbps")
            ydl.download([url])
            
        print(f"Download complete! File saved to {output_dir}")
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function to handle user interaction"""
    print("=" * 50)
    print("YouTube Audio Downloader")
    print("=" * 50)
    
    # Get YouTube URL from user
    youtube_url = input("Please enter YouTube video URL: ").strip()
    
    if not youtube_url:
        print("Error: Please enter a valid YouTube URL!")
        return
    
    # Get custom download directory (optional)
    custom_dir = input("Enter download directory (press Enter for default 'downloads'): ").strip()
    output_dir = custom_dir if custom_dir else "downloads"
    
    # Get audio quality (optional)
    quality_options = ["320", "256", "192", "128", "96", "64"]
    quality = input(f"Select audio quality in kbps ({'/'.join(quality_options)}) [default: 320]: ").strip()
    
    if not quality or quality not in quality_options:
        quality = "320"  # Default quality
    
    # Download the audio
    success = download_audio(youtube_url, output_dir, quality)
    
    if success:
        print("\nDownload successful!")
    else:
        print("\nDownload failed. Please check the URL and try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
