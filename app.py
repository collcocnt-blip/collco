from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Video Downloader Backend is Running!"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'URL missing hai!'}), 400

    # YouTube URL se extra parameters hatana
    if "youtube.com/watch" in url and "&" in url:
        url = url.split('&')[0]

    # YouTube Bot Block Bypass Options
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = yt_dlp.YoutubeDL({'quiet': True}).extract_info(url, download=False) if 'youtube' in url else ydl.extract_info(url, download=False)
            
            # Agar upar wale se na aaye toh android client ke sath extract karein
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_bypass:
                info = ydl_bypass.extract_info(url, download=False)

            download_url = info.get('url') or (info.get('formats')[0]['url'] if info.get('formats') else None)
            title = info.get('title', 'Downloaded Video')

            if download_url:
                return jsonify({
                    'success': True,
                    'title': title,
                    'download_url': download_url
                })
            else:
                return jsonify({'success': False, 'error': 'Direct download link nahi mil saka.'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': f'Server Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
