import os
import sys
import datetime
import time

def get_files(directory):
    files = []
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                os.stat(filepath)
                files.append(filepath)
            except FileNotFoundError:
                continue


    return files


def find_files_by_last_access(directory, days_ago):
    """
    Finds files in a given directory that were last accessed within a specified number of days.

    Args:
        directory (str): The path to the directory to search.
        days_ago (int): The number of days in the past to consider for last access.

    Returns:
        list: A list of file paths that meet the criteria.
    """
    found_files = []
    cutoff_timestamp = time.time() - (days_ago * 24 * 60 * 60) # Calculate cutoff timestamp

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                # Get file status information
                stat_info = os.stat(filepath)
                last_access_timestamp = stat_info.st_atime

                # Compare last access time with the cutoff
                if last_access_timestamp >= cutoff_timestamp:
                    found_files.append(filepath)
            except FileNotFoundError:
                # Handle cases where a file might be deleted between listing and stat call
                continue

    return found_files


if __name__ == '__main__':
    target_directory = sys.argv[1]
    days_to_check = int(sys.argv[2])
    accessed_files = get_files(target_directory)
    # accessed_files = find_files_by_last_access(target_directory, days_to_check)

    if accessed_files:
        print(f"Files last accessed within the last {days_to_check} days:")
        for file_path in accessed_files:
            print(file_path)
    else:
        print(f"No files found last accessed within the last {days_to_check} days.")
