import yt_dlp
import os


def download_audio(url, output_dir="downloads"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

        ydl_opts = {
            'format': 'bestaudio/best' ,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'nopllaylist': True,

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

if __name__ == "__main__":
    youtube_url = input("Lütfen YouTube vide URL'sini girin: ")

    if youtube_url:
        download_audio(youtube_url)
    else:
        print("Hata: Geçerli bir YouTube URL'si giriniz!")