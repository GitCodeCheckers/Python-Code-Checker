import os
import shutil
import sys

args = sys.argv[1:]
copied = []

def is_test_file(filename):
    """Return True if filename already matches pytest test naming conventions."""
    base = os.path.basename(filename)
    return base.startswith("test_") or base.endswith("_test.py")

def copy_file(src):
    base = os.path.basename(src)

    # Skip files already named like tests
    if is_test_file(base):
        print(f"[tox] Skipping already-valid test file: {src}")
        return

    new = f"test_{base}"
    shutil.copy(src, new)
    copied.append(new)
    print(f"[tox] Copied: {src} → {new}")

def walk_dir(path):
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".py"):
                full = os.path.join(root, f)
                copy_file(full)

print("[tox] Received args:", args)

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

# Save copied files for cleanup
with open(".tox_copied_files", "w") as f:
    for name in copied:
        f.write(name + "\n")
