#
# Scan Directory of photos and generate HTML files
#

import os

def is_image(file_name):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    return any(file_name.lower().endswith(ext) for ext in image_extensions)

def generate_gallery_index(root_dir, output_html):
    with open(output_html, 'w') as index_file:
        index_file.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Main Gallery</title>
        </head>
        <body>
            <h1>Main Gallery</h1>
            <ul>
        """)

        for subdir, dirs, _ in os.walk(root_dir):
            if subdir == root_dir:
                continue
            gallery_name = os.path.basename(subdir)
            gallery_file = f"{gallery_name}.html"
            index_file.write(f'<li><a href="{gallery_file}">{gallery_name}</a></li>\n')
            generate_sub_gallery(subdir, os.path.join(root_dir, gallery_file))

        index_file.write("""
            </ul>
        </body>
        </html>
        """)

def generate_sub_gallery(gallery_path, output_file):
    header = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Sub Gallery</title>
        <link rel="stylesheet" href="../photobox.css">
        <style>
            .gallery { display: flex; flex-wrap: wrap; }
            .gallery a { margin: 5px; border: 1px solid #ccc; display: inline-block; }
            .gallery img { width: 150px; height: 150px; object-fit: cover; }
        </style>
    </head>
    <body>
        <div class="gallery">
    """

    footer = """
        </div>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="../jquery.photobox.js"></script>
        <script>
            $(document).ready(function() {
                $('.gallery').photobox('a', { thumbs:true, loop:true });
            });
        </script>
    </body>
    </html>
    """

    with open(output_file, 'w') as f:
        f.write(header)

        for file in os.listdir(gallery_path):
            if is_image(file):
                file_path = os.path.join(gallery_path, file)
                relative_path = os.path.relpath(file_path, os.path.dirname(output_file))
                f.write(f'<a href="{relative_path}" target="_blank"><img src="{relative_path}" alt="{file}"></a>\n')

        f.write(footer)

root_directory = '/Users/james/Pictures/Photos/uploads'  # Replace with your gallery root directory
output_file = 'index.html'
generate_gallery_index(root_directory, output_file)

