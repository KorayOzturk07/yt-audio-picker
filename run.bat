@echo off
title YouTube Audio Downloader - Run Script

echo Installing required packages...
pip install yt-dlp ffmpeg

echo.

echo Checking for ffmpeg installation...
if exist "%~dp0\bin\ffmpeg.exe" (
    echo ffmpeg found in bin folder.
) else (
    echo ffmpeg not found in bin folder! Please ensure it's installed and the path is correct.
    pause  REM Pause to allow user to see the error message
)

echo.

echo Starting YouTube Audio Downloader...
python "%~dp0\main.py"

echo.

echo Script finished.
pause

