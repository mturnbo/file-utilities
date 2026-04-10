# File Utilities

A collection of Python utility scripts for file management.

## Scripts

### `recent-files.py`

Lists files in a directory that were accessed within the past N days, displayed in a formatted table sorted by most recent access time.

**Usage:**
```
python recent-files.py <directory> <days>
```

**Arguments:**
- `directory` — Path to the directory to search (searched recursively)
- `days` — Number of days to look back

**Example:**
```
python recent-files.py ~/Documents 7
```

**Output:**
```
Scanning files in the directory: ~/Documents accessed in the past 7 day(s)

File Name        |       File Size | Last Accessed
-----------------+-----------------+--------------------
report.pdf       |          45,234 | 2026-04-10 09:15:22
notes.txt        |           1,024 | 2026-04-09 14:30:01
-----------------+-----------------+--------------------

Total: 2 files found.
```

---

### `random-files.py`

Creates a random 2 KB text file with a random 12-character filename in each non-hidden subdirectory of the script's location. Useful for generating test data.

**Usage:**
```
python random-files.py
```

No arguments required. The script automatically discovers all non-hidden subdirectories relative to its own location and creates one `.txt` file per directory.

**Configuration** (edit constants at the top of the file):

| Constant | Default | Description |
|---|---|---|
| `FILE_SIZE_BYTES` | `2048` | Size of each generated file (~2 KB) |
| `FILENAME_LENGTH` | `12` | Length of the random filename (excluding `.txt`) |
| `MAX_ATTEMPTS` | `10` | Max tries to find a unique filename per directory |

## Requirements

- Python 3.x (no third-party dependencies)
