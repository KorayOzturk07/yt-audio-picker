@echo off
title YT Audio Picker
echo ===================================
echo          YT Audio Picker
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check if yt-dlp is installed
pip show yt-dlp >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing yt-dlp...
    pip install yt-dlp
    if %errorlevel% neq 0 (
        echo Failed to install yt-dlp. Please check your internet connection.
        pause
        exit /b 1
    )
)

REM Check if ffmpeg is in PATH
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg is not found in PATH. This is required for MP3 conversion.
    echo Please download FFmpeg from https://ffmpeg.org/download.html
    echo and add it to your system PATH.
    pause
    exit /b 1
)

REM Run the Python script
echo Starting YT Audio Picker...
python main.py

echo.
echo Process completed. Press any key to exit.
pause >nul
exit /b 0
