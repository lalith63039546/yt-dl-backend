from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "YT-DLP Video Downloader API is Running!"

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is required"}), 400

    command = f'yt-dlp -o "{DOWNLOAD_FOLDER}/%(title)s.%(ext)s" "{video_url}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        return jsonify({"message": "Download started", "output": result.stdout})
    else:
        return jsonify({"error": result.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

