#!/usr/bin/env python3

import argparse
import os
import sys
import time
from datetime import datetime

def get_files(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                os.stat(filepath)
                file_list.append(filepath)
            except FileNotFoundError:
                continue

    return file_list

def find_recently_accessed_files(directory, days):
    """
    Finds files in a given directory that were last accessed within a specified number of days.

    Args:
        directory (str): The path to the directory to search.
        days_ago (int): The number of days in the past to consider for last access.

    Returns:
        list: A list of file paths that meet the criteria.
    """

    now = time.time()
    cutoff = now - (days * 86400)

    recent_files = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)

            try:
                last_access_time = os.path.getatime(file_path)

                if last_access_time >= cutoff:
                    recent_files.append((file_path, last_access_time))

            except (FileNotFoundError, PermissionError):
                continue

    return recent_files


def print_table(files):
    # Sort by most recent access time (descending)
    files.sort(key=lambda x: x[1], reverse=True)

    # Format data
    formatted_rows = []
    for file_path, atime in files:
        file_name = os.path.basename(file_path)
        file_size = os.stat(file_path).st_size
        formatted_time = datetime.fromtimestamp(atime).strftime("%Y-%m-%d %H:%M:%S")
        formatted_rows.append((file_name, file_size, formatted_time))

    # Determine column widths
    file_name_col_width = max(len("File Name"), *(len(row[0]) for row in formatted_rows)) if formatted_rows else len("File Name")
    file_size_col_width = 15
    time_col_width = 20

    hr = f"{'-' * file_name_col_width}-+-{'-' * file_size_col_width}-+-{'-' * time_col_width}"

    # Header
    print(f"{'File Name'.ljust(file_name_col_width)} | {'File Size'.rjust(file_size_col_width)} | {'Last Accessed'}")
    print(hr)

    # Rows
    for file_name, file_size, access_time in formatted_rows:
        formatted_file_size = f"{file_size:,}"
        print(f"{file_name.ljust(file_name_col_width)} | {formatted_file_size.rjust(file_size_col_width)} | {access_time}")

    print(hr)
    print(f"\nTotal: {len(files)} files found.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find files accessed within the past N days."
    )
    parser.add_argument(
        "directory",
        help="Directory to search",
    )
    parser.add_argument(
        "days",
        type=int,
        help="Number of days to look back",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.", file=sys.stderr)
        return 1
    print(f"Scanning files in the directory: {args.directory} accessed in the past {args.days} day(s)\n")
    results = find_recently_accessed_files(args.directory, args.days)
    print_table(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
