import os

out_dir = os.path.join(os.path.dirname(__file__), "..", "out")

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
        f.write(f"Generated file {file_name}.sasm\n")