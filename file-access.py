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


def find_files_by_last_access(directory, days_ago):
    """
    Finds files in a given directory that were last accessed within a specified number of days.

    Args:
        directory (str): The path to the directory to search.
        days_ago (int): The number of days in the past to consider for last access.

    Returns:
        list: A list of file paths that meet the criteria.
    """
    file_list = []
    cutoff_timestamp = time.time() - (days_ago * 24 * 60 * 60) # Calculate cutoff timestamp

    for root, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                last_access_timestamp = os.path.getatime(file_path)
                if last_access_timestamp >= cutoff_timestamp:
                    file_list.append({
                        "file_name": name,
                        "last_accessed": datetime.fromtimestamp(last_access_timestamp),
                    }
                                     )
            except (FileNotFoundError, PermissionError):
                continue

    return file_list


if __name__ == '__main__':
    target_directory = sys.argv[1]
    days_to_check = int(sys.argv[2])

    print("Scanning files in the directory: ", target_directory, "accessed in the past ", days_to_check, " days")

    accessed_files = find_files_by_last_access(target_directory, days_to_check)

    if accessed_files:
        print(f"\nFiles last accessed within the last {days_to_check} days:\n")
        fmt = "{:<30} {:<15}"
        # Print Header
        print(fmt.format("File", "Last Accessed"))
        print("-" * 50)
        for file_path in accessed_files:
            print(fmt.format(file_path["file_name"], file_path["last_accessed"]))
        print("-" * 50)
    else:
        print(f"No files found last accessed within the last {days_to_check} days.")
