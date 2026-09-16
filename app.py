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

    # YouTube URL se playlist ya extra parameters hatane ke liye cleanup
    if "youtube.com" in video_url or "youtu.be" in video_url:
        video_url = re.sub(r"&list=[^&]+", "", video_url)
        video_url = re.sub(r"&index=[^&]+", "", video_url)

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
            # Agar direct stream url na mile toh formats se uthayein
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
    app.run(host='0.0.0.0', port=5000)
