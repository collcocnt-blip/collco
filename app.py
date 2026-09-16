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

    # Cobalt v10 Updated Active Instance
    cobalt_instances = [
        "https://api.cobalt.tools",
        "https://cobalt-api.kwiatek.xyz",
        "https://co.wuk.sh"
    ]

    payload = {
        "url": url,
        "videoQuality": "720"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    for instance in cobalt_instances:
        try:
            response = requests.post(instance, json=payload, headers=headers, timeout=8)
            data = response.json()

            # v10 Response format
            if response.status_code == 200 and data.get("status") in ["stream", "redirect", "tunnel"]:
                return jsonify({
                    'success': True,
                    'title': 'Downloaded Video',
                    'download_url': data.get("url")
                })
            elif response.status_code == 200 and data.get("url"):
                return jsonify({
                    'success': True,
                    'title': 'Downloaded Video',
                    'download_url': data.get("url")
                })
        except Exception:
            continue

    return jsonify({
        'success': False,
        'error': 'Video fetch nahi ho paya. Kripya link check karke dobara try karein.'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
