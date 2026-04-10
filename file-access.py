#!/usr/bin/env python3

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
        formatted_time = datetime.fromtimestamp(atime).strftime("%Y-%m-%d %H:%M:%S")
        file_name = os.path.basename(file_path)
        formatted_rows.append((file_name, formatted_time))

    # Determine column widths
    file_col_width = max(len("File Name"), *(len(row[0]) for row in formatted_rows)) if formatted_rows else len("File Name")
    time_col_width = 20

    # Header
    print(f"{'File Name'.ljust(file_col_width)} | {'Last Accessed'}")
    print(f"{'-' * file_col_width}-+-{'-' * time_col_width}")

    # Rows
    for file_name, access_time in formatted_rows:
        print(f"{file_name.ljust(file_col_width)} | {access_time}")

    print(f"\nTotal: {len(files)} files found.")


if __name__ == '__main__':
    target_directory = sys.argv[1]
    days = int(sys.argv[2])
    print(f"Scanning files in the directory: {target_directory} accessed in the past {days} day(s)\n")
    results = find_recently_accessed_files(target_directory, days)
    print_table(results)
