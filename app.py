from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Instagram & Media Downloader Backend is Running!"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'URL missing hai!'}), 400

    if "youtube.com" in url or "youtu.be" in url:
        return jsonify({'success': False, 'error': 'YouTube filhal supported nahi hai. Kripya Instagram ya Facebook ka link dalein.'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            download_url = info.get('url') or (info.get('formats')[0]['url'] if info.get('formats') else None)
            title = info.get('title', 'Social Media Video')
            thumbnail = info.get('thumbnail', '')  # Thumbnail URL fetch karega

            if download_url:
                return jsonify({
                    'success': True,
                    'title': title,
                    'download_url': download_url,
                    'thumbnail': thumbnail
                })
            else:
                return jsonify({'success': False, 'error': 'Video link extract nahi ho saka. Sahi post/reel ka link dalein.'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': f'Server Error: Sahi Reel ya Video ka direct link dalein.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
