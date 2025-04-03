import yt_dlp
import os
import sys
import re
from datetime import datetime
from typing import Optional, Tuple, List, Dict
from enum import Enum
import unicodedata
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


LANGUAGES = {
    'en': {
        'welcome': "YouTube Downloader",
        'select_language': "Select language / Dil seçin:",
        'enter_url': "Enter YouTube video/playlist URL:",
        'invalid_url': "Invalid YouTube URL. Please try again.",
        'download_dir': "Enter download directory (leave empty for 'downloads'):",
        'custom_filename': "Enter custom filename (without extension, leave empty for auto):",
        'select_format': "Select download format:",
        'format_audio': "Audio only (MP3)",
        'format_video': "Video with audio (MP4)",
        'select_quality': "Select quality:",
        'add_metadata': "Add metadata? (y/N):",
        'metadata_title': "Title:",
        'metadata_artist': "Artist:",
        'metadata_album': "Album:",
        'metadata_date': "Date (YYYY):",
        'download_start': "Downloading:",
        'download_complete': "Download complete!",
        'download_failed': "Download failed. Please check the URL and try again.",
        'thank_you': "Thank you for using YouTube Downloader!",
        'cancelled': "Operation cancelled by user.",
        'error': "An unexpected error occurred:",
        'playlist_download': "Playlist download started ({} videos)",
        'playlist_item': "Downloading {}/{}: {}",
        'available_formats': "Available formats:",
        'format_info': "{}. {} {} ({}MB)",
        'parallel_download': "Parallel download ({} threads)",
        'download_progress': "Progress: {}/{} completed ({} failed)",
        'ffmpeg_missing': "Warning: FFmpeg not found. Audio conversion may not work properly.",
        'checking_formats': "Checking available formats...",
        'best_quality': "Best available"
    },
    'tr': {
        'welcome': "YouTube İndirici",
        'select_language': "Dil seçin / Select language:",
        'enter_url': "YouTube video/playlist URL'sini girin:",
        'invalid_url': "Geçersiz YouTube URL'si. Lütfen tekrar deneyin.",
        'download_dir': "İndirme dizini (boş bırakırsanız 'downloads' kullanılır):",
        'custom_filename': "Özel dosya adı (uzantı olmadan, boş bırakırsanız otomatik):",
        'select_format': "İndirme formatı seçin:",
        'format_audio': "Sadece ses (MP3)",
        'format_video': "Sesli video (MP4)",
        'select_quality': "Kalite seçin:",
        'add_metadata': "Metadata eklemek istiyor musunuz? (e/H):",
        'metadata_title': "Başlık:",
        'metadata_artist': "Sanatçı:",
        'metadata_album': "Albüm:",
        'metadata_date': "Tarih (YYYY):",
        'download_start': "İndiriliyor:",
        'download_complete': "İndirme tamamlandı!",
        'download_failed': "İndirme başarısız. URL'yi kontrol edip tekrar deneyin.",
        'thank_you': "YouTube İndirici'yi kullandığınız için teşekkürler!",
        'cancelled': "Kullanıcı tarafından iptal edildi.",
        'error': "Beklenmeyen bir hata oluştu:",
        'playlist_download': "Playlist indirme başladı ({} video)",
        'playlist_item': "{}/{} indiriliyor: {}",
        'available_formats': "Mevcut formatlar:",
        'format_info': "{}. {} {} ({}MB)",
        'parallel_download': "Paralel indirme ({} thread)",
        'download_progress': "İlerleme: {}/{} tamamlandı ({} başarısız)",
        'ffmpeg_missing': "Uyarı: FFmpeg bulunamadı. Ses dönüşümü düzgün çalışmayabilir.",
        'checking_formats': "Mevcut formatlar kontrol ediliyor...",
        'best_quality': "En iyi kalite"
    }
}

class DownloadFormat(Enum):
    AUDIO = "audio"
    VIDEO = "video"

class AudioQuality(Enum):
    BEST = "320"
    HIGH = "256"
    MEDIUM = "192"
    STANDARD = "128"
    LOW = "96"
    POOR = "64"

class VideoQuality(Enum):
    ULTRA_HD = "2160"
    FULL_HD = "1080"
    HD = "720"
    SD = "480"
    LOW = "360"
    POOR = "240"

class Downloader:
    def __init__(self, language: str = 'en'):
        self.language = language
        self.translations = LANGUAGES.get(language, LANGUAGES['en'])
        self.lock = threading.Lock()
        self.success_count = 0
        self.failed_count = 0
        self.max_workers = 5  
        self.download_format = DownloadFormat.AUDIO
        self.audio_quality = AudioQuality.BEST
        self.video_quality = VideoQuality.HD
        self.ffmpeg_path = shutil.which('ffmpeg')
        if not self.ffmpeg_path:
            print(f"⚠️ {self.t('ffmpeg_missing')}")
    
    def t(self, key: str, *args) -> str:
        """Get translated string with optional formatting"""
        return self.translations.get(key, key).format(*args)

    def display_header(self):
        """Display fancy ASCII art header"""
        print(r"""
              
            __                __
   __  __  / /_  ____ _  ____/ /
  / / / / / __/ / __ `/ / __  / 
 / /_/ / / /_  / /_/ / / /_/ /  
 \__, /  \__/  \__,_/  \__,_/   
/____/                          

              
""".format(self.t('welcome')))

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename by removing invalid characters and normalizing unicode"""
        filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
        filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)
        return filename.strip()[:200]

    def get_available_formats(self, url: str) -> Optional[List[Tuple[str, str, str, int]]]:
        """Get available formats for a YouTube video"""
        try:
            print(f"⏳ {self.t('checking_formats')}")
            ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': False}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return None
                
                formats = []
                for f in info.get('formats', []):
                    if self.download_format == DownloadFormat.AUDIO and f.get('acodec') != 'none':
                        formats.append(
                            f.get('format_id', 'unknown'),
                            f.get('ext', 'unknown'),
                            f"{int(f.get('abr', 0))}kbps" if f.get('abr') else self.t('best_quality'),
                            int(f.get('filesize', f.get('filesize_approx', 0)) // (1024 * 1024)
                        ))
                    elif self.download_format == DownloadFormat.VIDEO and f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        formats.append(
                            f.get('format_id', 'unknown'),
                            f.get('ext', 'unknown'),
                            f"{f.get('height', '?')}p",
                            int(f.get('filesize', f.get('filesize_approx', 0)) // (1024 * 1024)
                        ))
                
                
                formats = list({f[0]: f for f in formats}.values())  
                if self.download_format == DownloadFormat.AUDIO:
                    formats.sort(key=lambda x: int(x[2].replace('kbps', '')) if 'kbps' in x[2] else 0, reverse=True)
                else:
                    formats.sort(key=lambda x: int(x[2].replace('p', '')) if x[2].endswith('p') else 0, reverse=True)
                
                return formats[:10]  
        except Exception as e:
            print(f"❌ Error getting available formats: {e}")
            return None

    def select_format(self) -> DownloadFormat:
        """Let user select download format"""
        print(f"\n{self.t('select_format')}")
        print(f"1. {self.t('format_audio')}")
        print(f"2. {self.t('format_video')}")
        
        while True:
            choice = input(f"\n{self.t('select_format')} (1-2, default=1): ").strip()
            if not choice:
                return DownloadFormat.AUDIO
            
            if choice == '1':
                return DownloadFormat.AUDIO
            elif choice == '2':
                return DownloadFormat.VIDEO
            print("Invalid choice. Please select 1-2.")

    def select_quality(self) -> None:
        """Interactive quality selection based on format"""
        if self.download_format == DownloadFormat.AUDIO:
            print(f"\n{self.t('select_quality')} (Audio)")
            for i, quality in enumerate(AudioQuality, 1):
                print(f"{i}. {quality.name.ljust(8)} - {quality.value}kbps")
            
            while True:
                try:
                    choice = input(f"\n{self.t('select_quality')} (1-6, default=1): ").strip()
                    if not choice:
                        self.audio_quality = AudioQuality.BEST
                        return
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(AudioQuality):
                        self.audio_quality = list(AudioQuality)[choice_idx]
                        return
                    print("Invalid choice. Please select 1-6.")
                except ValueError:
                    print("Please enter a number.")
        else:
            print(f"\n{self.t('select_quality')} (Video)")
            for i, quality in enumerate(VideoQuality, 1):
                print(f"{i}. {quality.name.ljust(8)} - {quality.value}p")
            
            while True:
                try:
                    choice = input(f"\n{self.t('select_quality')} (1-6, default=3): ").strip()
                    if not choice:
                        self.video_quality = VideoQuality.HD
                        return
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(VideoQuality):
                        self.video_quality = list(VideoQuality)[choice_idx]
                        return
                    print("Invalid choice. Please select 1-6.")
                except ValueError:
                    print("Please enter a number.")

    def download_single_file(self, url: str, output_dir: str, 
                           custom_filename: Optional[str], metadata: Optional[dict], 
                           item_num: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """Download a single file (audio or video) (thread-safe)"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            ydl_opts = {
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'progress_hooks': [self.progress_hook],
                'writethumbnail': True,
                'noprogress': True,
            }

            if self.download_format == DownloadFormat.AUDIO:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': self.audio_quality.value,
                    },
                    {'key': 'EmbedThumbnail'},
                    {'key': 'FFmpegMetadata'},
                ]
                ydl_opts['extractaudio'] = True
                ydl_opts['prefer_ffmpeg'] = True
                ydl_opts['ffmpeg_location'] = self.ffmpeg_path or ''
            else:
                
                ydl_opts['format'] = f'bestvideo[height<={self.video_quality.value}]+bestaudio/best[height<={self.video_quality.value}]'
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['postprocessors'] = [
                    {'key': 'EmbedThumbnail'},
                    {'key': 'FFmpegMetadata'},
                ]
                
                ydl_opts['format_sort'] = ['vcodec:h264', 'acodec:aac']
                ydl_opts['merge_output_format'] = 'mp4'

            if metadata:
                ydl_opts['postprocessor_args'] = [
                    '-metadata', f'title={metadata.get("title", "")}',
                    '-metadata', f'artist={metadata.get("artist", "")}',
                    '-metadata', f'album={metadata.get("album", "")}',
                    '-metadata', f'date={metadata.get("date", "")}',
                ]

            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return (False, None)
                
                title = info.get('title', 'Unknown Title')
                sanitized_title = self.sanitize_filename(title)
                
                if custom_filename:
                    sanitized_custom = self.sanitize_filename(custom_filename)
                    if item_num is not None:
                        ydl_opts['outtmpl'] = os.path.join(output_dir, f'{sanitized_custom}_{item_num:02d}.%(ext)s')
                    else:
                        ydl_opts['outtmpl'] = os.path.join(output_dir, f'{sanitized_custom}.%(ext)s')
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    if item_num is not None:
                        ydl_opts['outtmpl'] = os.path.join(output_dir, f'{sanitized_title}_{item_num:02d}_{timestamp}.%(ext)s')
                    else:
                        ydl_opts['outtmpl'] = os.path.join(output_dir, f'{sanitized_title}_{timestamp}.%(ext)s')

            with self.lock:
                print(f"\n📥 {self.t('download_start')} {title}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
                if self.download_format == DownloadFormat.AUDIO:
                    final_filename = os.path.splitext(filename)[0] + '.mp3'
                else:
                    final_filename = os.path.splitext(filename)[0] + '.mp4'
            
            with self.lock:
                print(f"✅ {title} {self.t('download_complete')}")
                self.success_count += 1
            return (True, final_filename)
        
        except yt_dlp.utils.DownloadError as e:
            with self.lock:
                print(f"❌ {title} {self.t('download_failed')}: {str(e)}")
                self.failed_count += 1
            return (False, None)
        except Exception as e:
            with self.lock:
                print(f"❌ {title} {self.t('error')}: {str(e)}")
                self.failed_count += 1
            return (False, None)

    def progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            with self.lock:
                percent = d.get('_percent_str', '?')
                speed = d.get('_speed_str', '?')
                eta = d.get('_eta_str', '?')
                print(f"\r↘️ Downloading: {percent} @ {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            with self.lock:
                print("\r", end='', flush=True)

    def download_playlist(self, url: str, output_dir: str, metadata: Optional[dict] = None) -> bool:
        """Download a YouTube playlist with parallel downloads"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info or 'entries' not in info:
                    return False
                
                playlist_title = info.get('title', 'Untitled Playlist')
                entries = info['entries']
                total_videos = len(entries)
                
                print(f"\n🎵 {self.t('playlist_download', total_videos)}: {playlist_title}")
                print(f"🚀 {self.t('parallel_download', min(self.max_workers, total_videos))}")
                
                self.success_count = 0
                self.failed_count = 0
                
                
                playlist_dir = os.path.join(output_dir, self.sanitize_filename(playlist_title))
                os.makedirs(playlist_dir, exist_ok=True)
                
                with ThreadPoolExecutor(max_workers=min(self.max_workers, total_videos)) as executor:
                    futures = []
                    for i, entry in enumerate(entries, 1):
                        video_url = entry.get('url')
                        if not video_url:
                            continue
                        
                        futures.append(
                            executor.submit(
                                self.download_single_file,
                                video_url,
                                playlist_dir,
                                None,
                                metadata,
                                i
                            )
                        )
                    
                    for future in as_completed(futures):
                        
                        pass
                
                print(f"\n🎉 {self.t('download_progress', self.success_count, total_videos, self.failed_count)}")
                return self.success_count > 0
        except Exception as e:
            print(f"\n❌ {self.t('error')} {str(e)}")
            return False

    def validate_url(self, url: str) -> bool:
        """Validate YouTube URL"""
        patterns = [
            r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$',
            r'^https?:\/\/(youtu\.be\/|(www\.)?youtube\.com\/(embed\/|v\/|watch\?v=|watch\?.+&v=|playlist\?list=))([\w-]+)(.+)?$'
        ]
        return any(re.match(pattern, url) for pattern in patterns)

    def is_playlist(self, url: str) -> bool:
        """Check if URL is a playlist"""
        return 'playlist?list=' in url.lower()

    def select_language(self) -> str:
        """Language selection menu"""
        print("\n" + "="*50)
        print(self.t('select_language'))
        print("="*50)
        print("1. English")
        print("2. Türkçe")
        
        while True:
            choice = input("Seçim / Choice (1-2): ").strip()
            if choice == '1':
                return 'en'
            elif choice == '2':
                return 'tr'
            print("Geçersiz seçim / Invalid choice")

    def main(self):
        """Main application flow"""
        try:
            
            self.language = self.select_language()
            self.translations = LANGUAGES.get(self.language, LANGUAGES['en'])
            
            self.display_header()
            
            
            while True:
                url = input(f"\n🎵 {self.t('enter_url')} ").strip()
                if self.validate_url(url):
                    break
                print(f"❌ {self.t('invalid_url')}")

            
            self.download_format = self.select_format()
            
            
            if not self.is_playlist(url):
                formats = self.get_available_formats(url)
                if formats:
                    print(f"\nℹ️ {self.t('available_formats')}")
                    for i, (format_id, ext, quality, size) in enumerate(formats[:5], 1):
                        print(self.t('format_info', i, ext.upper(), quality, size))

            
            self.select_quality()
            
            
            custom_dir = input(f"\n📁 {self.t('download_dir')} ").strip()
            output_dir = os.path.expanduser(custom_dir) if custom_dir else "downloads"
            
            custom_filename = input(f"\n✏️ {self.t('custom_filename')} ").strip()
            if not custom_filename:
                custom_filename = None
            
            metadata = {}
            if input(f"\n➕ {self.t('add_metadata')} ").strip().lower() in ('y', 'e'):
                metadata['title'] = input(f"{self.t('metadata_title')} ").strip()
                metadata['artist'] = input(f"{self.t('metadata_artist')} ").strip()
                metadata['album'] = input(f"{self.t('metadata_album')} ").strip()
                metadata['date'] = input(f"{self.t('metadata_date')} ").strip()

            
            print("\n" + "="*50)
            if self.is_playlist(url):
                success = self.download_playlist(url, output_dir, metadata)
            else:
                success, filepath = self.download_single_file(url, output_dir, custom_filename, metadata)
                if success and filepath:
                    print(f"\n🎧 {self.t('download_complete')}:\n{os.path.abspath(filepath)}")
            
            if not success:
                print(f"\n❌ {self.t('download_failed')}")
            
            print(f"\n{self.t('thank_you')}")
        
        except KeyboardInterrupt:
            print(f"\n\n🛑 {self.t('cancelled')}")
            sys.exit(0)
        except Exception as e:
            print(f"\n\n💥 {self.t('error')} {e}")
            sys.exit(1)

if __name__ == "__main__":
    downloader = Downloader()
    downloader.main()