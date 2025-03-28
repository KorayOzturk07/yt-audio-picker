@echo off
cls
echo [INFO] Checking system requirements...
echo --------------------------------------


where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Python not found. Installing Python...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)


echo [INFO] Installing required Python packages...
pip install yt-dlp >nul 2>&1


if not exist "ffmpeg\ffmpeg.exe" (
    echo [INFO] Downloading FFmpeg...
    mkdir ffmpeg
    curl -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    tar -xf ffmpeg.zip -C ffmpeg --strip-components=1
    del ffmpeg.zip
)


setx PATH "%CD%\ffmpeg;%PATH%"

echo [INFO] All dependencies installed. Starting yt-audio-picker...
python main.py

pause
