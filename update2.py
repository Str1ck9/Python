#
# update script to add gallery-style.css to all html files
#

import os

def add_css_to_html(root_dir, css_file):
    css_link = f'<link rel="stylesheet" href="{css_file}">\n'

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    content = f.readlines()

                # Check if CSS link already exists
                if css_link not in content:
                    # Insert the CSS link after the <head> tag
                    for i, line in enumerate(content):
                        if '<head>' in line:
                            content.insert(i + 1, css_link)
                            break

                with open(file_path, 'w') as f:
                    f.writelines(content)
                print(f"Updated {file_path}")

root_directory = '/Users/james/Pictures/Photos/uploads'  # Your root directory
css_file = 'gallery-style.css'  # Name of your CSS file
add_css_to_html(root_directory, css_file)

