@echo off
chcp 65001 >nul
rem Сборка Autosalon.exe (запускать на Windows из папки проекта)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name Autosalon main.py
echo.
echo Готово: dist\Autosalon.exe
pause
