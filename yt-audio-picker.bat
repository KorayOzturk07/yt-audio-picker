@echo off
cls
echo Checking system requirements...
echo --------------------------------------

:: 1. Python Yüklü mü Kontrol Et
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not installed. Downloading Python...
    start https://www.python.org/downloads/
    exit
)

:: 2. Gerekli Kütüphaneleri Kur
echo Installing required Python packages...
pip install yt-dlp >nul 2>&1

:: 3. FFmpeg Yüklü mü Kontrol Et
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] FFmpeg not found. Downloading FFmpeg...
    start https://ffmpeg.org/download.html
    exit
)

:: 4. Programı Başlat
echo All dependencies are installed. Starting yt-audio-picker...
python main.py

:: 5. Terminali Açık Tut
pause
