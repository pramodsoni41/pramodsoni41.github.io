@echo off
echo Installing dependencies...
pip install pyinstaller requests keyring pillow pystray

echo.
echo Building exe...
pyinstaller --onefile --noconsole --name "IITBHU_Sync" sync_iitbhu.py

echo.
echo Done! Exe is in the "dist" folder.
pause
