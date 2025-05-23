from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_GROUP_ID = os.environ.get("LINE_GROUP_ID")

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot webhook running"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.json
    print("Received event:", data)
    return jsonify(data)

def send_image_to_line(img_url):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "to": LINE_GROUP_ID,
        "messages": [
            {
                "type": "image",
                "originalContentUrl": img_url,
                "previewImageUrl": img_url
            }
        ]
    }
    resp = requests.post("https://api.line.me/v2/bot/message/push", json=body, headers=headers)
    return resp.json()

@app.route("/send-image", methods=["POST"])
def send_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400

    image = request.files['image']
    filename = image.filename
    save_path = f"static/{filename}"
    os.makedirs("static", exist_ok=True)
    image.save(save_path)

    image_url = request.host_url + save_path

    result = send_image_to_line(image_url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
