#!/usr/bin/env python3

import os
import random
import string

# Configuration
FILE_SIZE_BYTES = 2048   # ~2 KB
FILENAME_LENGTH = 12     # length of random filename (without .txt)
MAX_ATTEMPTS = 10        # safety limit per directory

def generate_random_text(size: int) -> str:
    chars = string.ascii_letters + string.digits + "     \n"
    return "".join(random.choice(chars) for _ in range(size))

def generate_random_filename(length: int) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length)) + ".txt"

def pick_unique_path(directory: str) -> str:
    for _ in range(MAX_ATTEMPTS):
        candidate = os.path.join(directory, generate_random_filename(FILENAME_LENGTH))
        if not os.path.exists(candidate):
            return candidate
    raise RuntimeError(
        f"Could not find a unique filename in '{directory}' after {MAX_ATTEMPTS} attempts."
    )

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for entry in os.listdir(script_dir):
        # Skip hidden folders (starting with ".")
        if entry.startswith("."):
            continue

        path = os.path.join(script_dir, entry)

        if os.path.isdir(path):
            file_path = pick_unique_path(path)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(generate_random_text(FILE_SIZE_BYTES))

            print(f"Created {file_path}")

if __name__ == "__main__":
    main()
