pyinstaller --onefile src/torambot.py --icon=icon.ico
RMDIR /S /Q "dist/data"
XCOPY "data" "dist/data" /S /E /I
COPY "settings.json" "dist/settings.json" /b/v/y