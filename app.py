import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "API Active & Ready!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL missing'}), 400

    try:
        # Rapid Public Engine for Instagram/YouTube Bypass
        api_url = f"https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url,
            "vQuality": "max"
        }

        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        data = response.json()

        if response.status_code == 200 and data.get("url"):
            return jsonify({
                'success': True,
                'title': 'Downloaded Video',
                'download_url': data.get("url")
            })
        else:
            # Fallback direct response
            return jsonify({
                'success': False,
                'error': data.get("text", "Video fetch nahi ho paya. URL private ho sakta hai.")
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Server Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
