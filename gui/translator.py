import json
import os

LANG_DIR = os.path.join(os.path.dirname(__file__), 'i18n')
DEFAULT_LANG = 'en'

_cached_translations = {}


def load_language(lang_code):
    if lang_code in _cached_translations:
        return _cached_translations[lang_code]

    lang_path = os.path.join(LANG_DIR, f'{lang_code}.json')
    if not os.path.isfile(lang_path):
        print(f"⚠️ Language file not found: {lang_path}. Falling back to English.")
        lang_path = os.path.join(LANG_DIR, f'{DEFAULT_LANG}.json')

    try:
        with open(lang_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            _cached_translations[lang_code] = translations
            return translations
    except Exception as e:
        print(f"❌ Failed to load language file '{lang_code}': {e}")
        return {}