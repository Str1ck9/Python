#
# Fix the path issues for css and js in a folder of html files
#

import os

def update_html_files(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    content = f.read()

                # Replace the relative paths
                content = content.replace('<link rel="stylesheet" href="../photobox.css">', '<link rel="stylesheet" href="photobox.css">')
                content = content.replace('<script src="../jquery.photobox.js"></script>', '<script src="jquery.photobox.js"></script>')

                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"Updated {file_path}")

root_directory = '/Users/james/Pictures/Photos/uploads'  # Your root directory
update_html_files(root_directory)

