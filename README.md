## 📦 FiveM Vehicle Packer

Easy-to-use GUI tool to convert GTA V vehicle mods into ready-to-use FiveM resources.
Drag and drop a car mod folder, and get a complete FiveM-compatible resource in seconds.

## 🚀 Features
✅ Convert .meta, .yft, .ytd, and other mod files into FiveM resource format
- 🧠 Automatically detects vehicle model name from vehicles.meta
- 🧼 Stream and data folder setup
- 📝 Auto-generates fxmanifest.lua and vehicle_names.lua
- 🎨 Light and dark theme support
- 📂 Drag & drop or mod folders
- 🕘 Remembers recently converted resources

## 📥 Download
You can grab the latest .exe from the Releases tab.

## 💻 How to Use (From Source)
1. Install Python 3.11+
2. Run in PS or cmd.
```bash
pip install -r requirements.txt
```
3. Run the app:
```bash
python main.py
-- or
py main.py
```
## 🛠 Build .exe Version (Optional)
To package the app for Windows (standalone executable):
```bash
pyinstaller --noconfirm --onefile --windowed main.py
```
Or use build.bat to automate the process.

## 🧰 Planned Features
- Batch conversion support (multiple assets to one resource)
- ~~Multilingual support (currently only in English)~~
- Include support for audio files

## ❤️ Credits
- Built with Python + PyQt6
- This is my first time using Python, so be gentle on me and please provide any feedback!
