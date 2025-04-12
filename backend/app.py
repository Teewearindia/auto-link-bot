from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import requests
import json
import os

from config import VERIFY_TOKEN, ACCESS_TOKEN, GRAPH_URL, INSTAGRAM_ID

app = Flask(__name__)
CORS(app)

# 🔹 Initialize Firebase
def init_firebase():
    try:
        if firebase_admin._apps:
            return
        if os.path.exists("serviceAccountKey.json"):
            with open("serviceAccountKey.json", "r") as f:
                cred_dict = json.load(f)
        else:
            firebase_json = os.getenv("FIREBASE_KEY")
            cred_dict = json.loads(firebase_json)

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://instaautobot-57f40-default-rtdb.firebaseio.com/'
        })

    except Exception as e:
        print("❌ Firebase init failed:", str(e))

init_firebase()

@app.route('/')
def home():
    return "🔥 Insta Auto Link Bot with Firebase", 200

@app.route('/save_mapping', methods=['POST'])
def save_mapping():
    data = request.json
    post_id = data.get("post_id")
    link = data.get("link")

    ref = db.reference(f"/mappings/{post_id}")
    ref.set(link)

    return jsonify({"message": "✅ Mapping saved to Firebase"}), 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403

    if request.method == 'POST':
        data = request.get_json()
        print("📩 Webhook received:")
        print(json.dumps(data, indent=2))

        try:
            entry = data.get("entry", [])[0]
            change = entry.get("changes", [])[0]
            value = change.get("value", {})

            comment = value.get("text", "")
            user_id = value.get("from", {}).get("id")
            comment_id = value.get("id")
            post_id = value.get("post_id")

            if any(word in comment.lower() for word in ["link", "buy", "price"]):
                ref = db.reference(f"/mappings/{post_id}")
                product_url = ref.get()

                if product_url:
                    send_dm(user_id, product_url)
                    reply_to_comment(comment_id, "Check your DM! 👋")

        except Exception as e:
            print("❌ Webhook handling error:", str(e))

        return "ok", 200

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
        print("📬 DM Status:", res.status_code)
        print("📬 DM Response:", res.text)
    except Exception as e:
        print("❌ DM error:", str(e))

def reply_to_comment(comment_id, text):
    url = f"{GRAPH_URL}/{comment_id}/replies"
    payload = {
        "message": text,
        "access_token": ACCESS_TOKEN
    }

    try:
        res = requests.post(url, data=payload)
        print("💬 Comment Reply Status:", res.status_code)
        print("💬 Comment Reply Response:", res.text)
    except Exception as e:
        print("❌ Comment reply error:", str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
