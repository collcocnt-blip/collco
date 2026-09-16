import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "API is Live & Running!"})

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL Missing", "success": False}), 400

    if "youtube.com" in video_url or "youtu.be" in video_url:
        video_url = re.sub(r"&list=[^&]+", "", video_url)
        video_url = re.sub(r"&index=[^&]+", "", video_url)

    # yt-dlp options with cookies file to bypass bot check
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',  # Yeh line bot error ko hata देगी
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
            if not download_url and 'formats' in info:
                download_url = info['formats'][-1].get('url')

            return jsonify({
                "success": True,
                "download_url": download_url,
                "title": info.get('title', 'Video')
            })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
