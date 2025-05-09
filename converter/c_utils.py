import os
import re

MODEL_NAME_REGEX = re.compile(r"<modelName>\s*(.*?)\s*</modelName>", re.IGNORECASE)
AUDIO_NAME_REGEX = re.compile(r"<audioNameHash>\s*(.*?)\s*</audioNameHash>", re.IGNORECASE)

def parse_model_names_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return MODEL_NAME_REGEX.findall(content)


def parse_model_names_from_content(content):
    return MODEL_NAME_REGEX.findall(content)


def extract_audio_name_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = AUDIO_NAME_REGEX.search(content)
    return match.group(1).strip().lower() if match else None


def get_fallback_model_name(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".yft") and "_hi" not in file.lower():
                return os.path.splitext(file)[0]
    return "unknown_model"


def generate_vehicle_names_lua(output_folder, model_names):
    lua_path = os.path.join(output_folder, "vehicle_names.lua")
    with open(lua_path, "w", encoding="utf-8") as f:
        for name in sorted(model_names):
            f.write(f"AddTextEntry('{name}', '{name}')\n")


def write_fxmanifest(output_path, meta_files):
    fxmanifest_path = os.path.join(output_path, "fxmanifest.lua")
    audio_path = os.path.join(output_path, "audioconfig")

    with open(fxmanifest_path, "w", encoding="utf-8") as f:
        f.write("fx_version 'cerulean'\ngame 'gta5'\n\nfiles {\n")
        for meta in meta_files:
            f.write(f"    'data/{meta}',\n")
        f.write("    'audioconfig/*.rel',\n")
        f.write("    'sfx/**/*.awc'\n")
        f.write("}\n\n")

        for meta in meta_files:
            if meta == "vehicles.meta":
                f.write("data_file 'VEHICLE_METADATA_FILE' 'data/vehicles.meta'\n")
            elif meta == "handling.meta":
                f.write("data_file 'HANDLING_FILE' 'data/handling.meta'\n")
            elif meta == "carvariations.meta":
                f.write("data_file 'VEHICLE_VARIATION_FILE' 'data/carvariations.meta'\n")
            elif meta == "carcols.meta":
                f.write("data_file 'CARCOLS_FILE' 'data/carcols.meta'\n")
            elif meta == "dlctext.meta":
                f.write("data_file 'DLCTEXT_FILE' 'data/dlctext.meta'\n")

        if os.path.exists(audio_path):
            for name in os.listdir(audio_path):
                if name.endswith(".dat151.rel"):
                    f.write(f"data_file 'AUDIO_GAMEDATA' 'audioconfig/{name}'\n")
                elif name.endswith(".dat54.rel"):
                    f.write(f"data_file 'AUDIO_SOUNDDATA' 'audioconfig/{name}'\n")
                elif name.endswith(".dat10.rel"):
                    f.write(f"data_file 'AUDIO_SYNTHDATA' 'audioconfig/{name}'\n")

        model = "unknown"
        sfx_root = os.path.join(output_path, "sfx")
        if os.path.exists(sfx_root):
            for name in os.listdir(sfx_root):
                if name.startswith("dlc_"):
                    model = name[4:]
                    break
        f.write(f"data_file 'AUDIO_WAVEPACK' 'sfx/dlc_{model}'\n")
        f.write("\nclient_script 'vehicle_names.lua'\n")


def merge_meta_files(meta_type, file_paths):
    tags = {
        "vehicles.meta": ("<CVehicleModelInfo__InitDataList>", "</CVehicleModelInfo__InitDataList>"),
        "handling.meta": ("<CHandlingDataMgr>", "</CHandlingDataMgr>"),
        "carvariations.meta": ("<CVehicleModelInfoVariation>", "</CVehicleModelInfoVariation>"),
        "carcols.meta": ("<CVehicleModelInfoVarGlobal>", "</CVehicleModelInfoVarGlobal>"),
        "dlctext.meta": ("<CExtraTextMetaFile>", "</CExtraTextMetaFile>"),
        "vehiclelayouts.meta": ("<CVehicleMetadataMgr>", "</CVehicleMetadataMgr>")
    }[meta_type]

    open_tag, close_tag = tags
    content_list = [open_tag]

    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        inner = re.findall(f"<{open_tag.strip('<>')}[^>]*?>(.*?)</{close_tag.strip('</>')}>", content, re.DOTALL | re.IGNORECASE)
        if inner:
            content_list.append(inner[0].strip())

    content_list.append(close_tag)
    return '\n'.join(content_list)