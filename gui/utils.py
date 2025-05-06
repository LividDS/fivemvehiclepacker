import os
import json
import sys
import subprocess

SETTINGS_PATH = os.path.join(os.getenv("APPDATA") or os.getenv("HOME"), "fivem_converter_settings.json")

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(data):
    try:
        with open(SETTINGS_PATH, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass

def open_folder(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])
    except Exception as e:
        print(f"Error opening folder: {e}")

def get_theme_styles(mode):
    if mode == "dark":
        return {
            "bg": "#121212",
            "fg": "#ffffff",
            "input_bg": "#1e1e1e",
            "input_fg": "#dddddd",
            "border": "#aaa",
            "button_bg": "#2e2e2e",
            "button_fg": "#ffffff",
            "button_hover": "#3399ff"
        }
    else:
        return {
            "bg": "#ffffff",
            "fg": "#000000",
            "input_bg": "#f0f0f0",
            "input_fg": "#000000",
            "border": "#888",
            "button_bg": "#e0e0e0",
            "button_fg": "#000000",
            "button_hover": "#3399ff"
        }