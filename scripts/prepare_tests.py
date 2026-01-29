import os
import shutil
import sys

args = sys.argv[1:]
copied = []

def copy_file(src):
    base = os.path.basename(src)
    new = f"test_{base}"
    shutil.copy(src, new)
    copied.append(new)
    print(f"[tox] Copied: {src} → {new}")

def walk_dir(path):
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".py"):
                copy_file(os.path.join(root, f))

if not args:
    print("[tox] No files or directories passed — using pytest auto-discovery.")
else:
    for path in args:
        if os.path.isdir(path):
            print(f"[tox] Recursively scanning directory: {path}")
            walk_dir(path)
        elif os.path.isfile(path):
            copy_file(path)
        else:
            print(f"[tox] Warning: {path} does not exist and will be ignored.")

with open(".tox_copied_files", "w") as f:
    for name in copied:
        f.write(name + "\n")
