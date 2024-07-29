import yt_dlp

# Function to download YouTube video
def download_youtube_video(url, save_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("Download completed")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
url = 'https://www.youtube.com/watch?v=2YHChQ9RbHw'
save_path = './'  # Save in the current directory

download_youtube_video(url, save_path)
