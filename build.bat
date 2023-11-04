RMDIR /S /Q "build"
RMDIR /S /Q "dist"
pyinstaller pybot/main.py --clean --onefile --console ^
	--name="pybot" ^
	--collect-submodules="pybot" ^
	--icon="logo.ico" 
	--target-architecture="x86_64"
XCOPY "scripts" "dist/scripts" /S /E /I
COPY "settings.json" "dist/settings.json" /b/v/y