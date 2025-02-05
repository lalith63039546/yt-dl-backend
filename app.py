from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Ensure the downloads folder exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "YouTube Video Downloader API is running!"})

@app.route("/download", methods=["GET"])
def download_video():
    video_url = request.args.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    # yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best',
        'noplaylist': True,
        'quiet': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
