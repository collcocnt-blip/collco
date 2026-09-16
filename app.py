import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import yt_dlp

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

    clean_url = re.sub(r"&list=[^&]+", "", video_url)
    clean_url = re.sub(r"&index=[^&]+", "", clean_url)

    # --- YOUTUBE: Direct Secure API (Bypasses Bot Check completely) ---
    if "youtube.com" in video_url or "youtu.be" in video_url:
        try:
            api_endpoint = f"https://api.vkrdown.com/v1/download?url={clean_url}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(api_endpoint, headers=headers, timeout=10)
            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                d_url = data.get("data", {}).get("downloads", [{}])[0].get("url") or data.get("data", {}).get("url")
                if d_url:
                    return jsonify({
                        "success": True,
                        "download_url": d_url,
                        "title": data.get("data", {}).get("title", "YouTube Video")
                    })
        except Exception:
            pass

        # Backup YouTube API if first fails
        try:
            backup_api = f"https://api.downloadall.workers.dev/?url={clean_url}"
            b_resp = requests.get(backup_api, timeout=8)
            b_data = b_resp.json()
            if b_resp.status_code == 200 and (b_data.get("url") or b_data.get("download_url")):
                return jsonify({
                    "success": True,
                    "download_url": b_data.get("url") or b_data.get("download_url"),
                    "title": "YouTube Video"
                })
        except Exception:
            pass

        return jsonify({"error": "YouTube video fetch nahi ho saka. Kripya doosra link try karein.", "success": False}), 500

    # --- INSTAGRAM & OTHERS: yt-dlp ---
    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url') or info['formats'][-1].get('url')
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
