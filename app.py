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

    # yt-dlp options for normal video downloads
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,  # Download single video, not a playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information and start download
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        return send_file(filename, as_attachment=True)

    except yt_dlp.utils.DownloadError as e:
        # If there's a CAPTCHA or login required, handle the error
        if "Sign in to confirm you're not a bot" in str(e):
            return "Download failed: YouTube requires login or CAPTCHA verification for this video. Please try another video.", 400
        return f"Download failed: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
