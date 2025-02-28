import fnmatch
import os


def get_video_id(url:str):
    if "v=" in url:
        return url.split("v=")[1][:11]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1][:11]
    raise ValueError("Invalid URL format. Please provide a valid YouTube URL.")

def find_matching_files(pattern: str, directory: str = "."):
    """
    Finds all files in the given directory (and subdirectories) that match the given pattern.

    :param pattern: The pattern to match (e.g., "*.txt", "report_*").
    :param directory: The directory to search in (default: current directory).
    :return: A list of matching file paths.
    """
    matching_files = []
    for root, _, files in os.walk(directory):
        print(root)
        for filename in fnmatch.filter(files, pattern):
            matching_files.append(os.path.join(root, filename))
    return matching_files