import os
import shutil
import re


def parse_model_names(vehicles_meta_path):
    with open(vehicles_meta_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(r"<modelName>\s*(.*?)\s*</modelName>", content)


def generate_vehicle_names_lua(output_folder, model_names):
    lua_path = os.path.join(output_folder, "vehicle_names.lua")
    with open(lua_path, "w", encoding="utf-8") as f:
        for name in model_names:
            f.write(f"AddTextEntry('{name}', '{name}')\n")


def build_fivem_resource(extracted_path, output_path, resource_name):
    stream_path = os.path.join(output_path, "stream")
    data_path = os.path.join(output_path, "data")
    os.makedirs(stream_path, exist_ok=True)
    os.makedirs(data_path, exist_ok=True)

    meta_files = []
    stream_files = []

    vehicles_meta = None
    for root, _, files in os.walk(extracted_path):
        for file in files:
            if file == "vehicles.meta":
                vehicles_meta = os.path.join(root, file)
                break

    model_names = parse_model_names(vehicles_meta) if vehicles_meta else []

    for root, _, files in os.walk(extracted_path):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith((".yft", ".ytd", ".ydr", ".ymt", ".awc")):
                shutil.copy(full_path, os.path.join(stream_path, file))
                stream_files.append(file)
            elif file.endswith(".meta"):
                shutil.copy(full_path, os.path.join(data_path, file))
                meta_files.append(file)

    fxmanifest_path = os.path.join(output_path, "fxmanifest.lua")
    with open(fxmanifest_path, "w", encoding="utf-8") as f:
        f.write(f"""fx_version 'cerulean'
game 'gta5'

files {{
""")
        for meta in meta_files:
            f.write(f"    'data/{meta}',\n")
        f.write("}\n\n")

        for meta in meta_files:
            if "vehicles.meta" in meta:
                f.write("data_file 'VEHICLE_METADATA_FILE' 'data/vehicles.meta'\n")
            elif "handling.meta" in meta:
                f.write("data_file 'HANDLING_FILE' 'data/handling.meta'\n")
            elif "carvariations.meta" in meta:
                f.write("data_file 'VEHICLE_VARIATION_FILE' 'data/carvariations.meta'\n")
            elif "carcols.meta" in meta:
                f.write("data_file 'CARCOLS_FILE' 'data/carcols.meta'\n")
            elif "dlctext.meta" in meta:
                f.write("data_file 'DLCTEXT_FILE' 'data/dlctext.meta'\n")
        f.write("\nclient_script 'vehicle_names.lua'\n")

    if model_names:
        generate_vehicle_names_lua(output_path, model_names)

    return stream_files, meta_files
