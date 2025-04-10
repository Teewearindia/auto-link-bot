import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://instaautobot-57f40-default-rtdb.firebaseio.com/'  # 🔁 Replace with actual URL
        })
        print("✅ Firebase initialized")
    except Exception as e:
        print("❌ Firebase init failed:", str(e))
