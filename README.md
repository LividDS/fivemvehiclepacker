# 📦 FiveM Vehicle Packer

FiveM Vehicle Packer is an intuitive GUI tool that streamlines the conversion of GTA V vehicle mods into FiveM-ready resources. With a simple drag-and-drop interface, it automates the setup process, allowing you to integrate custom vehicles into your FiveM server effortlessly.
*Built with Python + PyQt6.*

## 🚀 Features
- **Automated Conversion:** Compile loose `.meta`, `.yft`, `.ytd` into a FiveM-compatible resource format.
- **Auto-Generated Files:** Creates `fxmanifest.lua` and `vehicle_names.lua` files.
- **Resource Structuring:** Sets up `stream` and `data` folders with corresponding files.

## 📥 Download
You can grab the latest .exe from the Releases section.

## 🛠️ Installation
- Install Python 3.11 or higher
### Steps
1. Clone the Repository:
```bash
git clone https://github.com/LividDS/fivemvehiclepacker.git
cd fivemvehiclepacker
```
2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r dev-requirements.txt
```
3. Run the app:
```bash
python main.py
# or
py main.py
```

## 🛠️ Build .exe Version (Optional)
To package the app for Windows (standalone executable):
```bash
pyinstaller --noconfirm --onefile --windowed main.py
```
Or use build.bat to automate the process.

## 📦 Output Structure
When conversion is done, this is what your output should look like:
```kotlin
myvehicle/
├── fxmanifest.lua
├── vehicle_names.lua
├── data/
│   ├── vehicles.meta
│   ├── handling.meta
│   ├── carcols.meta
│   ├── carvariations.meta
│   ├── dlctext.meta
├── stream/
│   ├── mycar.yft
│   ├── mycar_hi.yft
│   ├── mycar.ytd
│   ├── interior.ytd
│   ├── mycar.ymt
├── audioconfig/
│   ├── mycar_game.dat151.rel
│   ├── mycar_sounds.dat54.rel
│   ├── mycar_game.dat151.nametable
│   ├── mycar_sounds.dat54.nametable
├── sfx/
│   └── dlc_mycar/
│       ├── mycar.awc
│       └── mycar_npc.awc
```

## 🧰 Planned Features
- Batch conversion support. (multiple assets to one resource)
- ~~Multilingual support. (currently only in English)~~
- Include support for audio files.

## 🤝 Contributing
Contributions are welcome! If you have suggestions, encounter issues, or want to enhance the tool.
