@echo off
echo 🧹 Cleaning up old builds...
rmdir /s /q dist
rmdir /s /q build

echo 🛠️  Building main.exe (onefile)...
pyinstaller --noconfirm --onefile --console ^
  --add-data "gui/i18n/en.json;gui/i18n" ^
  --add-data "gui/i18n/de.json;gui/i18n" ^
  --add-data "gui/i18n/fr.json;gui/i18n" ^
  --add-data "gui/i18n/es.json;gui/i18n" ^
  --add-data "gui;gui" ^
  --hidden-import PyQt6.QtWidgets ^
  --hidden-import PyQt6.QtGui ^
  --hidden-import PyQt6.QtCore ^
  main.py

echo ✅ Done! Your single executable is at dist\main.exe
start dist
pause
