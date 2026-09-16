from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # Cross-Origin Enabled

@app.route('/download', methods=['GET'])
def get_download_url():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({'success': False, 'error': 'URL is missing'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            return jsonify({
                'success': True,
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'downloadUrl': info.get('url', '')
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Server running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)