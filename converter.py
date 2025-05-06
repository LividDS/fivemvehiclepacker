import os
import shutil
import re

MODEL_NAME_REGEX = re.compile(r"<modelName>\s*(.*?)\s*</modelName>", re.IGNORECASE)

def parse_model_names_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return MODEL_NAME_REGEX.findall(content)

def parse_model_names_from_content(content):
    return MODEL_NAME_REGEX.findall(content)

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
    with open(fxmanifest_path, "w", encoding="utf-8") as f:
        f.write("fx_version 'cerulean'\ngame 'gta5'\n\nfiles {\n")
        for meta in meta_files:
            f.write(f"    'data/{meta}',\n")
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
        f.write("\nclient_script 'vehicle_names.lua'\n")

def build_fivem_resource(extracted_path, output_path):
    stream_path = os.path.join(output_path, "stream")
    data_path = os.path.join(output_path, "data")
    os.makedirs(stream_path, exist_ok=True)
    os.makedirs(data_path, exist_ok=True)

    meta_files, stream_files = [], []
    model_names = set()
    found_model = False

    for root, _, files in os.walk(extracted_path):
        for file in files:
            full_path = os.path.join(root, file)
            if file == "vehicles.meta":
                try:
                    parsed = parse_model_names_from_file(full_path)
                    if parsed:
                        model_names.update(parsed)
                        found_model = True
                except Exception as e:
                    print(f"Failed to parse model names: {e}")
            if file.endswith((".yft", ".ytd", ".ydr", ".ymt", ".awc")):
                shutil.copy(full_path, os.path.join(stream_path, file))
                stream_files.append(file)
            elif file.endswith(".meta"):
                shutil.copy(full_path, os.path.join(data_path, file))
                meta_files.append(file)

    if not found_model:
        fallback = get_fallback_model_name(extracted_path)
        print(f"\u26a0\ufe0f Using fallback model name: {fallback}")
        model_names.add(fallback)

    write_fxmanifest(output_path, meta_files)

    if model_names:
        generate_vehicle_names_lua(output_path, model_names)

    return stream_files, meta_files

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

def build_combined_fivem_resource(vehicle_folders, output_path):
    os.makedirs(output_path, exist_ok=True)
    stream_path = os.path.join(output_path, "stream")
    data_path = os.path.join(output_path, "data")
    os.makedirs(stream_path, exist_ok=True)
    os.makedirs(data_path, exist_ok=True)

    meta_files_dict = {
        "vehicles.meta": [],
        "handling.meta": [],
        "carvariations.meta": [],
        "carcols.meta": [],
        "dlctext.meta": [],
        "vehiclelayouts.meta": []
    }
    model_names = set()

    for folder in vehicle_folders:
        vehicle_name = os.path.basename(folder)
        vehicle_stream_path = os.path.join(stream_path, vehicle_name)
        os.makedirs(vehicle_stream_path, exist_ok=True)

        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith((".yft", ".ytd", ".ydr", ".ymt", ".awc")):
                    shutil.copy(full_path, os.path.join(vehicle_stream_path, file))
                elif file in meta_files_dict:
                    meta_files_dict[file].append(full_path)
                    if file == "vehicles.meta":
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                model_names.update(parse_model_names_from_content(f.read()))
                        except Exception as e:
                            print(f"Failed to parse model names in {file}: {e}")

    saved_meta_files = []
    for meta_name, paths in meta_files_dict.items():
        if paths:
            merged = merge_meta_files(meta_name, paths)
            target = os.path.join(data_path, meta_name)
            with open(target, 'w', encoding='utf-8') as f:
                f.write(merged)
            saved_meta_files.append(meta_name)

    write_fxmanifest(output_path, saved_meta_files)

    if model_names:
        generate_vehicle_names_lua(output_path, model_names)

    all_streamed = [os.path.join(d, f) for d in os.listdir(stream_path)
                    for f in os.listdir(os.path.join(stream_path, d))]
    return all_streamed, saved_meta_files