from .c_utils import (
    parse_model_names_from_content,
    generate_vehicle_names_lua,
    merge_meta_files,
    write_fxmanifest
)
import os
import shutil


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
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith((".yft", ".ytd", ".ydr", ".ymt", ".awc")):
                    shutil.copy(full_path, os.path.join(stream_path, file))
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

    all_streamed = []
    for dirpath, _, filenames in os.walk(stream_path):
        for f in filenames:
            all_streamed.append(os.path.join(dirpath, f))

    return all_streamed, saved_meta_files