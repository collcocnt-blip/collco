from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Isse CORS error bilkul khatam ho jayega

@app.route('/')
def home():
    return jsonify({"status": "Backend Server Alive & Ready!"})

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL Dena zaroori hai!"}), 400

    url = "https://instagram-downloader-scraper-reels-igtv-posts-stories.p.rapidapi.com/v1/post-info"
    querystring = {"code_or_id_or_url": video_url}

    headers = {
        "x-rapidapi-key": "f45ea9e0a0mshe8d905b180aa394p19ed0fjsn9d332668c767",
        "x-rapidapi-host": "instagram-downloader-scraper-reels-igtv-posts-stories.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
