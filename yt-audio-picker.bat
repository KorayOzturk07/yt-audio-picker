@echo off
setlocal enabledelayedexpansion

echo [INFO] Fixing FFmpeg installation...
echo --------------------------------------


set "CURRENT_DIR=%CD%"


where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Python not found. Installing Python...
    curl -L -o "%CURRENT_DIR%\python_installer.exe" https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    "%CURRENT_DIR%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1
    del "%CURRENT_DIR%\python_installer.exe"
    echo [INFO] Python installed successfully.
) else (
    echo [INFO] Python already installed.
)


echo [INFO] Installing/Upgrading yt-dlp...
pip install --upgrade yt-dlp
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install yt-dlp.
    pause
    exit /b 1
)


echo [INFO] Downloading FFmpeg...
set "FFMPEG_DIR=%CURRENT_DIR%\ffmpeg"
if not exist "%FFMPEG_DIR%" mkdir "%FFMPEG_DIR%"

if not exist "%FFMPEG_DIR%\bin\ffmpeg.exe" (
    :: Download a more reliable direct link
    curl -L -o "%CURRENT_DIR%\ffmpeg.zip" "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n6.1-latest-win64-gpl-6.1.zip"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to download FFmpeg.
        pause
        exit /b 1
    )
    
    
    echo [INFO] Extracting FFmpeg...
    powershell -Command "Expand-Archive -Path '%CURRENT_DIR%\ffmpeg.zip' -DestinationPath '%FFMPEG_DIR%' -Force"
    if %errorlevel% neq 0 (
        echo [WARNING] PowerShell extraction failed, trying alternative method...
        :: Try another PowerShell approach
        powershell -Command "& {Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%CURRENT_DIR%\ffmpeg.zip', '%FFMPEG_DIR%')}"
        if %errorlevel% neq 0 (
            echo [ERROR] Failed to extract FFmpeg using PowerShell.
            echo [INFO] Please extract the ffmpeg.zip file manually.
            pause
            exit /b 1
        )
    )
    
    :: Clean up
    del "%CURRENT_DIR%\ffmpeg.zip"
)


set "FFMPEG_BIN="
for /r "%FFMPEG_DIR%" %%G in (ffmpeg.exe) do (
    set "FFMPEG_BIN=%%~dpG"
    goto found_ffmpeg
)

:found_ffmpeg
if not defined FFMPEG_BIN (
    echo [ERROR] Could not find FFmpeg executable.
    echo [INFO] Please download FFmpeg manually from https://ffmpeg.org/download.html
    pause
    exit /b 1
)

echo [INFO] FFmpeg found at: %FFMPEG_BIN%


set "PATH=%FFMPEG_BIN%;%PATH%"


where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] FFmpeg is still not accessible in the PATH.
    echo [INFO] Creating a launcher batch file that will set the PATH correctly.
) else (
    echo [INFO] FFmpeg is accessible in the current PATH.
)


echo [INFO] Creating launcher...
echo @echo off > "%CURRENT_DIR%\run-yt-audio-picker.bat"
echo cd /d "%CURRENT_DIR%" >> "%CURRENT_DIR%\run-yt-audio-picker.bat"
echo set "PATH=%FFMPEG_BIN%;%%PATH%%" >> "%CURRENT_DIR%\run-yt-audio-picker.bat"
echo python main.py >> "%CURRENT_DIR%\run-yt-audio-picker.bat"
echo pause >> "%CURRENT_DIR%\run-yt-audio-picker.bat"


if not exist "%CURRENT_DIR%\main.py" (
    echo [WARNING] main.py not found in the current directory.
    echo [INFO] Please make sure main.py is in the same folder as this script.
)

echo [SUCCESS] Setup complete!
echo FFmpeg has been installed to: %FFMPEG_DIR%
echo A launcher "run-yt-audio-picker.bat" has been created in the current folder.
echo.
echo [INFO] Would you like to run the program now? (Y/N)
choice /c YN /n
if %errorlevel% equ 1 (
    cd /d "%CURRENT_DIR%"
    set "PATH=%FFMPEG_BIN%;%PATH%"
    python main.py
)

pause
exit /b 0
