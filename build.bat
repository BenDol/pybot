RMDIR /S /Q "build"
RMDIR /S /Q "dist"
pyinstaller --onefile src/torambot.py --icon=icon.ico
XCOPY "scripts" "dist/scripts" /S /E /I
COPY "settings.json" "dist/settings.json" /b/v/y