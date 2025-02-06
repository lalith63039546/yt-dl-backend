from flask import Flask, request, send_file, jsonify
import subprocess
import os
import re

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "YT-DLP Video Downloader API is Running!"

@app.route("/download", methods=["GET"])
def download_video():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify({"error": "URL parameter is required"}), 400

    # Use yt-dlp to get the title
    title_command = f'yt-dlp --get-filename -o "%(title)s.%(ext)s" "{video_url}"'
    title_result = subprocess.run(title_command, shell=True, capture_output=True, text=True)
    
    if title_result.returncode != 0:
        return jsonify({"error": title_result.stderr}), 500

    # Clean filename to avoid special character issues
    filename = title_result.stdout.strip()
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)  # Remove invalid filename characters
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    # Download video using yt-dlp with bypass options
    command = f'yt-dlp --no-check-certificate --cookies-from-browser firefox -o "{filepath}" "{video_url}"'
    download_result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if download_result.returncode == 0:
        return send_file(filepath, as_attachment=True)  # Serve the file for direct download
    else:
        return jsonify({"error": download_result.stderr}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
