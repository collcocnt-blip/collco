import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "Server Active"})

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'URL missing'}), 400

    # Fallback Public Extraction Endpoints (Proxy Supported)
    endpoints = [
        f"https://api.cobalt.tools/api/json",
        f"https://co.wuk.sh/api/json"
    ]

    payload = {
        "url": video_url,
        "vQuality": "720"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Attempt 1: Universal Multi-Engine Fetch
    for ep in endpoints:
        try:
            res = requests.post(ep, json=payload, headers=headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                dl_link = data.get("url")
                if dl_link:
                    return jsonify({
                        'success': True,
                        'title': 'Video Download',
                        'download_url': dl_link
                    })
        except Exception:
            continue

    # Attempt 2: Backup Scraper API (Works for YT & Insta)
    try:
        backup_api = f"https://api.downloadall.workers.dev/?url={video_url}"
        b_res = requests.get(backup_api, timeout=10)
        b_data = b_res.json()
        
        final_link = b_data.get("url") or b_data.get("download_url")
        if final_link:
            return jsonify({
                'success': True,
                'title': 'Video Download',
                'download_url': final_link
            })
    except Exception as e:
        pass

    return jsonify({
        'success': False,
        'error': 'Video fetch nahi ho saka. Kripya URL check karein ya dusra link try karein.'
    }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
