from .c_utils import (
    parse_model_names_from_file,
    get_fallback_model_name,
    generate_vehicle_names_lua,
    write_fxmanifest,
    extract_audio_name_from_file
)
import os
import shutil


def build_fivem_resource(extracted_path, output_path):
    stream_path = os.path.join(output_path, "stream")
    data_path = os.path.join(output_path, "data")
    audio_path = os.path.join(output_path, "audioconfig")
    sfx_path = os.path.join(output_path, "sfx")
    os.makedirs(stream_path, exist_ok=True)
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(audio_path, exist_ok=True)

    meta_files = []
    stream_files = []
    model_names = set()
    audio_name = None
    audio_files = []

    for root, _, files in os.walk(extracted_path):
        for file in files:
            full_path = os.path.join(root, file)
            lower = file.lower()

            if file == "vehicles.meta":
                try:
                    model_names.update(parse_model_names_from_file(full_path))
                    audio_name = extract_audio_name_from_file(full_path)
                except Exception as e:
                    print(f"Error parsing model or audio name: {e}")

            if lower.endswith((".yft", ".ytd", ".ydr", ".ymt")):
                target_file = os.path.join(stream_path, file)
                if not os.path.exists(target_file):
                    shutil.copy(full_path, target_file)
                    stream_files.append(file)

            elif file in {
                "vehicles.meta", "handling.meta", "carvariations.meta",
                "carcols.meta", "dlctext.meta", "vehiclelayouts.meta"
            }:
                shutil.copy(full_path, os.path.join(data_path, file))
                meta_files.append(file)

            elif lower.endswith(".rel") or "nametable" in lower:
                shutil.copy(full_path, os.path.join(audio_path, file))
                audio_files.append(file)

            elif lower.endswith(".awc"):
                name = audio_name if audio_name else (list(model_names)[0] if model_names else "vehicle")
                sfx_target = os.path.join(sfx_path, f"dlc_{name}")
                os.makedirs(sfx_target, exist_ok=True)
                shutil.copy(full_path, os.path.join(sfx_target, file))
                audio_files.append(file)

    if not model_names:
        fallback = get_fallback_model_name(extracted_path)
        print(f"\u26a0\ufe0f Using fallback model name: {fallback}")
        model_names.add(fallback)

    if model_names:
        generate_vehicle_names_lua(output_path, model_names)

    write_fxmanifest(output_path, meta_files)

    return stream_files, meta_files, audio_files