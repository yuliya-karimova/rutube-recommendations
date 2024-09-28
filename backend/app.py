from flask import Flask, request, jsonify, session, send_from_directory, abort
from flask_cors import CORS
import json
from modules.video import get_top_videos, get_related_videos, get_recommended_videos

app = Flask(__name__, static_folder='dist')
CORS(app, supports_credentials=True, origins=["http://localhost:5174", "http://localhost:3000", "http://localhost:5173"])

@app.route("/rutube-recommendations/")
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/top-videos', methods=['GET'])
def get_top_videos_endpoint():
    client_id = request.args.get('client_id')
    try:
        res = get_top_videos()
        return jsonify({"data": res})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/related-videos', methods=['GET'])
def get_related_videos_endpoint():
    client_id = request.args.get('client_id')
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "Выберите видео."}), 400
    
    try:
        res = get_related_videos(video_id)
        return jsonify({"data": res})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/recommended-videos', methods=['GET'])
def get_recommended_videos_endpoint():
    client_id = request.args.get('client_id')
    video_id = request.args.get('video_id')
    reaction = request.args.get('reaction')
    if not video_id:
        return jsonify({"error": "Выберите видео."}), 400
    
    try:
        res = get_recommended_videos(video_id, reaction, client_id)
        return jsonify({"data": res})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)