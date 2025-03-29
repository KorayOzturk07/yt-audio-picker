@echo off
cls
echo [INFO] Sistem gereksinimleri kontrol ediliyor...
echo --------------------------------------


where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Python bulunamadı. Python yükleniyor...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)


echo [INFO] Gerekli Python paketleri yükleniyor...
pip install yt-dlp >nul 2>&1


set FFMPEG_DIR=%CD%\ffmpeg
if not exist "%FFMPEG_DIR%\ffmpeg.exe" (
    echo [INFO] FFmpeg indiriliyor...
    curl -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    mkdir "%FFMPEG_DIR%"
    tar -xf ffmpeg.zip -C "%FFMPEG_DIR%" --strip-components=1
    del ffmpeg.zip
)


setx PATH "%FFMPEG_DIR%;%PATH%"


echo [INFO] Lütfen komut istemcisini kapatıp yeniden açın veya aşağıdaki komutu çalıştırarak PATH değişikliklerini uygulayın:
echo set PATH=%FFMPEG_DIR%;%PATH%
pause


echo [INFO] Tüm bağımlılıklar yüklendi. yt-audio-picker başlatılıyor...
python main.py


pause
