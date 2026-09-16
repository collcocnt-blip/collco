import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "API is Active"})

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL Required", "success": False}), 400

    # Hum yahan free public Cobalt API instance use kar rahe hain jo YouTube/Instagram ko bina bot error ke direct fetch kar leta hai
    cobalt_url = "https://co.wuk.sh/api/json"
    
    payload = {
        "url": video_url,
        "vQuality": "720"
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(cobalt_url, json=payload, headers=headers, timeout=10)
        res_data = response.json()

        if response.status_code == 200 and ("url" in res_data or "picker" in res_data):
            final_url = res_data.get("url") or res_data.get("picker")[0].get("url")
            return jsonify({
                "success": True,
                "video_url": final_url,
                "title": "Downloaded Video"
            })
        else:
            err_msg = res_data.get("text", "Could not fetch video")
            return jsonify({"success": False, "error": err_msg}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
