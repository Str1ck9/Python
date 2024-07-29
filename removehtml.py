# Deletes all html files recursively

import os

def remove_html_files(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(subdir, file)
                print(f"Deleting: {file_path}")  # Optional: prints the path of the file being deleted
                os.remove(file_path)

root_directory = '/Users/james/Pictures/Photos/uploads'  # Replace with your directory path
remove_html_files(root_directory)

