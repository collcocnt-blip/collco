import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import requests
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

    # --- YOUTUBE KE LIYE DIRECT PUBLIC API (No Bot Error, No Cookies Needed) ---
    if "youtube.com" in video_url or "youtu.be" in video_url:
        try:
            clean_url = re.sub(r"&list=[^&]+", "", video_url)
            clean_url = re.sub(r"&index=[^&]+", "", clean_url)
            
            payload = {"url": clean_url, "vQuality": "720"}
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            
            response = requests.post("https://co.wuk.sh/api/json", json=payload, headers=headers, timeout=10)
            res_data = response.json()

            if response.status_code == 200 and ("url" in res_data or "picker" in res_data):
                final_download_url = res_data.get("url") or res_data.get("picker")[0].get("url")
                return jsonify({
                    "success": True,
                    "download_url": final_download_url,
                    "title": res_data.get("filename", "YouTube Video")
                })
        except Exception as e:
            pass  # Agar yahan issue aaye toh niche fallback chalega

    # --- INSTAGRAM AUR BAAKI APPS KE LIYE AAPKA PURANA YT-DLP METHOD ---
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
