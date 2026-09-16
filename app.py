import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# Enable CORS for all domains so your website can talk to this API
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "API is Live & Running!",
        "message": "Send video link to /download?url=YOUR_LINK"
    })

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL missing in request'}), 400

    # Advanced yt-dlp configuration to bypass blocks & extract direct MP4 links
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extract Direct Stream URL
            video_url = info.get('url')
            if not video_url and 'formats' in info:
                # Fallback to last format if direct url isn't in root
                video_url = info['formats'][-1].get('url')

            return jsonify({
                'success': True,
                'title': info.get('title', 'Video Download'),
                'thumbnail': info.get('thumbnail', ''),
                'download_url': video_url
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Render environmental PORT bind for 0.0.0.0 host
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
