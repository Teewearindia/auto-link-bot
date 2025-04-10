from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import requests
import json
from config import VERIFY_TOKEN, ACCESS_TOKEN, GRAPH_URL, INSTAGRAM_ID

app = Flask(__name__)
CORS(app)

# 🔹 Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id.firebaseio.com/'  # ⬅️ Replace with yours
})

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
        print("📩 Webhook data:", json.dumps(data, indent=2))

        try:
            entry = data.get("entry", [])[0]
            change = entry.get("changes", [])[0]
            value = change.get("value", {})

            comment = value.get("text", "")
            user_id = value.get("from", {}).get("id")
            post_id = value.get("post_id")

            if "link" in comment.lower():
                ref = db.reference(f"/mappings/{post_id}")
                product_url = ref.get()

                if product_url:
                    send_dm(user_id, product_url)
        except Exception as e:
            print("❌ Error:", str(e))

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
        print("📬 DM Sent:", res.status_code, res.text)
    except Exception as e:
        print("❌ DM Send Error:", str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
