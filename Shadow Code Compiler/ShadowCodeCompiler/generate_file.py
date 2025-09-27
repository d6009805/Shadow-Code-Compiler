import os

out_dir = os.path.join(os.path.dirname(__file__), "..", "out")
prohibited_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
prohibited_names = [
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
]
def gen_file(file_name, compiled_code):
    os.makedirs(out_dir, exist_ok=True)
    file_name = os.path.splitext(str(file_name))[0]
    full_path = os.path.join(out_dir, file_name + ".sasm")
    compiled_code = str(compiled_code)
    with open(full_path, 'w') as f:
        f.write(compiled_code)
    print(f"Generated file {file_name}.sasm")

def log_file(file_name):
    os.makedirs(out_dir, exist_ok=True)
    file_name = os.path.splitext(str(file_name))[0]
    full_path = os.path.join(os.path.dirname(__file__), "files_created.log")
    with open(full_path, 'a') as f:
        f.write(f"Generated file '{file_name}.sasm'\n")

def is_valid_filename(name):
    if any(ch in name for ch in prohibited_chars):
        return False
    base_name = name.split(".")[0].upper()
    if base_name in prohibited_names:
        return False
    return True
