import asyncio
from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Video download function with format selection
async def download_video_async(video_url, video_format):
    output_path = "downloads/%(title)s.%(ext)s"
    ydl_opts = {
        'format': video_format,  # Use the format passed by the user
        'outtmpl': output_path,
        'cookiefile': 'cookies.txt',  # Optional: for authentication cookies
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'extractaudio': False,
        'noprogress': True,
        'postprocessors': [],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)
        return filename
    except Exception as e:
        return f"Download failed: {str(e)}"

@app.route('/download', methods=['GET'])
async def download_video():
    video_url = request.args.get('url')
    video_format = request.args.get('format', 'best')  # Default to 'best' if no format is provided
    
    if not video_url:
        return "Error: No video URL provided.", 400

    # Check if the format is valid (optional, you can add more validation)
    valid_formats = ['360p', '480p', '720p', '1080p', 'best']
    if video_format not in valid_formats:
        return "Error: Invalid video format.", 400

    filename = await download_video_async(video_url, video_format)
    if 'Download failed' in filename:
        return filename, 500

    return jsonify({"download_url": filename})

if __name__ == '__main__':
    os.makedirs("downloads", exist_ok=True)
    app.run(host='0.0.0.0', port=5000, threaded=True)
