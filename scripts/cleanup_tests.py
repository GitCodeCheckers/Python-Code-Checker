import os

if os.path.exists(".tox_copied_files"):
    with open(".tox_copied_files") as f:
        for line in f:
            name = line.strip()
            if os.path.exists(name):
                os.remove(name)
                print(f"[tox] Cleaned up: {name}")
    os.remove(".tox_copied_files")
