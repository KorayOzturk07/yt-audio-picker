@echo off
cls
echo [INFO] Checking system requirements...
echo --------------------------------------


echo yt-audio-picker log file > yt-audio-picker.log
echo %date% %time% >> yt-audio-picker.log


where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Python not found. Installing Python...
    echo Python not found. Attempting to install... >> yt-audio-picker.log
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to download Python installer. >> yt-audio-picker.log
        echo [ERROR] Failed to download Python installer. Please check your internet connection.
        goto error
    )
    echo Running Python installer... >> yt-audio-picker.log
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo [ERROR] Python installation failed. >> yt-audio-picker.log
        echo [ERROR] Python installation failed. Please try installing Python manually.
        goto error
    )
    del python_installer.exe
)


echo [INFO] Installing required Python packages...
echo Installing required Python packages... >> yt-audio-picker.log
pip install yt-dlp 
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install yt-dlp. >> yt-audio-picker.log
    echo [ERROR] Failed to install yt-dlp. Please check your internet connection.
    goto error
)


set FFMPEG_DIR=%CD%\ffmpeg
if not exist "%FFMPEG_DIR%\bin\ffmpeg.exe" (
    echo [INFO] Downloading FFmpeg...
    echo Downloading FFmpeg... >> yt-audio-picker.log
    
    
    curl -L -o ffmpeg.zip https://github.com/GyanD/codexffmpeg/releases/download/2023-03-05-git-912ac82f3c/ffmpeg-6.0-full_build.zip
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to download FFmpeg. >> yt-audio-picker.log
        echo [ERROR] Failed to download FFmpeg. Please check your internet connection.
        goto error
    )
    
    echo Creating FFmpeg directory... >> yt-audio-picker.log
    mkdir "%FFMPEG_DIR%" 2>nul
    
    echo Extracting FFmpeg using PowerShell... >> yt-audio-picker.log
    powershell -command "& {Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('ffmpeg.zip', '%FFMPEG_DIR%')}"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to extract FFmpeg using PowerShell. >> yt-audio-picker.log
        echo [ERROR] Failed to extract FFmpeg. Trying alternative method...
        
        
        echo Trying alternative extraction method... >> yt-audio-picker.log
        powershell -command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '%FFMPEG_DIR%' -Force"
        if %errorlevel% neq 0 (
            echo [ERROR] All extraction methods failed. >> yt-audio-picker.log
            echo [ERROR] Failed to extract FFmpeg. Please extract the zip file manually.
            goto error
        )
    )
    
    del ffmpeg.zip
    
    
    echo Locating FFmpeg binaries... >> yt-audio-picker.log
    set "FFMPEG_BIN="
    for /r "%FFMPEG_DIR%" %%G in (ffmpeg.exe) do (
        set "FFMPEG_BIN=%%~dpG"
        echo Found FFmpeg at: %%~dpG >> yt-audio-picker.log
        goto ffmpeg_found
    )
    
    if not defined FFMPEG_BIN (
        echo [ERROR] Could not locate FFmpeg binary in extracted files. >> yt-audio-picker.log
        echo [ERROR] Could not locate FFmpeg binary in extracted files.
        goto error
    )
    
    :ffmpeg_found
    echo FFmpeg found at: %FFMPEG_BIN% >> yt-audio-picker.log
    
    
    set "PATH=%FFMPEG_BIN%;%PATH%"
    
    
    echo Adding FFmpeg to system PATH... >> yt-audio-picker.log
    setx PATH "%FFMPEG_BIN%;%PATH%" >nul
    if %errorlevel% neq 0 (
        echo [WARNING] Failed to update PATH environment variable. >> yt-audio-picker.log
        echo [WARNING] Failed to update PATH environment variable. 
        echo [WARNING] You may need to add FFmpeg to your PATH manually.
    )
)


echo [INFO] Verifying FFmpeg installation...
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    
    for /r "%FFMPEG_DIR%" %%G in (ffmpeg.exe) do (
        set "FFMPEG_BIN=%%~dpG"
        set "PATH=%FFMPEG_BIN%;%PATH%"
        echo [INFO] Found FFmpeg at: %%~dpG
        echo Found and added FFmpeg to current PATH: %%~dpG >> yt-audio-picker.log
        goto verify_again
    )
    
    :verify_again
    where ffmpeg >nul 2>nul
    if %errorlevel% neq 0 (
        echo [WARNING] FFmpeg is not accessible in the current PATH. >> yt-audio-picker.log
        echo [WARNING] FFmpeg is not accessible in the current PATH.
        echo [WARNING] You may need to restart the command prompt or add FFmpeg to your PATH manually.
    )
)


if not exist "main.py" (
    echo [ERROR] main.py not found in the current directory. >> yt-audio-picker.log
    echo [ERROR] main.py not found in the current directory.
    echo Please make sure the main.py file is in the same folder as this batch file.
    goto error
)


echo [INFO] All dependencies installed. Starting yt-audio-picker...
echo Starting yt-audio-picker... >> yt-audio-picker.log
python main.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run main.py. >> yt-audio-picker.log
    echo [ERROR] Failed to run main.py. 
    goto error
)

echo [INFO] Program completed successfully. >> yt-audio-picker.log
goto end

:error
echo [ERROR] An error occurred during setup. See yt-audio-picker.log for details.
echo Please try to run the script again or install the dependencies manually.

:end
echo [INFO] Press any key to exit...
pause > nul
