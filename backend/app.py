from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests  # ✅ ADD MISSING IMPORT

from config import VERIFY_TOKEN, ACCESS_TOKEN, GRAPH_URL, INSTAGRAM_ID

app = Flask(__name__)
CORS(app)

# Load mapping file or create if doesn't exist
if not os.path.exists("post_map.json"):
    with open("post_map.json", "w") as f:
        json.dump({}, f)

@app.route('/')
def home():
    return "🔥 Insta Auto Link Bot Backend Running!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403

    if request.method == 'POST':
        data = request.json
        print("📩 Received webhook data:", json.dumps(data, indent=2))  # ✅ For debug

        try:
            entry = data.get("entry", [])[0]
            change = entry.get("changes", [])[0]
            value = change.get("value", {})

            comment = value.get("text", "")
            user_id = value.get("from", {}).get("id")
            post_id = value.get("post_id")

            if "link" in comment.lower():
                with open("post_map.json", "r") as f:
                    post_map = json.load(f)

                product_url = post_map.get(post_id)

                if product_url:
                    send_dm(user_id, product_url)
        except Exception as e:
            print("❌ Error handling webhook:", str(e))

        return "ok", 200

@app.route('/save_mapping', methods=['POST'])
def save_mapping():
    data = request.json
    post_id = data.get("post_id")
    link = data.get("link")

    with open("post_map.json", "r+") as f:
        post_map = json.load(f)
        post_map[post_id] = link
        f.seek(0)
        json.dump(post_map, f, indent=2)
        f.truncate()

    return jsonify({"message": "✅ Mapping saved"}), 200

def send_dm(user_id, text):
    url = f"{GRAPH_URL}/{INSTAGRAM_ID}/messages"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE",
        "access_token": ACCESS_TOKEN
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        print("📬 DM Sent:", res.status_code, res.text)
    except Exception as e:
        print("❌ DM Error:", str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
