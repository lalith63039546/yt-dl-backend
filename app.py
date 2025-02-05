from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return "Error: URL is required!", 400

    # Create downloads folder if not exists
    os.makedirs("downloads", exist_ok=True)

    # yt-dlp options to bypass restrictions like age check
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,  # Ensure single video download, not a playlist
        'age_limit': 18,     # Handle age-restricted videos
        'geo_bypass': True,  # Bypass region restrictions
        'restrictfilenames': True,  # Prevent unusual characters in filenames
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Download failed: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
