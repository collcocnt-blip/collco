import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "API is Active & Running!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL missing'}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        # Direct Universal Scraper API
        api_url = f"https://api.vkrdown.com/v1/download?url={url}"
        response = requests.get(api_url, headers=headers, timeout=12)
        data = response.json()

        # Check response status
        if response.status_code == 200 and data.get("status") == "success":
            download_url = None
            if data.get("data", {}).get("downloads"):
                download_url = data["data"]["downloads"][0].get("url")
            elif data.get("data", {}).get("url"):
                download_url = data["data"]["url"]

            if download_url:
                return jsonify({
                    'success': True,
                    'title': data.get("data", {}).get("title", "Social Media Video"),
                    'thumbnail': data.get("data", {}).get("thumbnail", ""),
                    'download_url': download_url
                })

        # Alternative Backup Engine
        backup_url = f"https://api.downloadall.workers.dev/?url={url}"
        b_resp = requests.get(backup_url, headers=headers, timeout=10)
        b_data = b_resp.json()

        if b_resp.status_code == 200 and (b_data.get("url") or b_data.get("download_url")):
            return jsonify({
                'success': True,
                'title': 'Video Download',
                'download_url': b_data.get("url") or b_data.get("download_url")
            })

        return jsonify({
            'success': False,
            'error': 'Video fetch nahi ho saka. Kripya valid public URL daalein.'
        }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server Connection Timeout: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
