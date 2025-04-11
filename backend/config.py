import os
import json
import base64
import firebase_admin
from firebase_admin import credentials

# Base64 encoded Firebase key from environment variable
firebase_json = base64.b64decode(os.getenv("FIREBASE_KEY")).decode("utf-8")
firebase_dict = json.loads(firebase_json)

# Initialize Firebase app
cred = credentials.Certificate(firebase_dict)
firebase_admin.initialize_app(cred)

# Instagram API config
VERIFY_TOKEN = "instaverify123"
ACCESS_TOKEN = "EAAH1Wpp5TgUBO88ArQd3Ely5KAJFaW7q6XUHFM4SkWXlPyRka4xenrr4PSN9MUagd3Wps4I8h4f7ZA5YH5kZBBbrvB6MwZCVnPXcJiEco3YPmxPyHnejisP63do1BSR3YE14jhsUDDwy745c7ciJu4rntvdmqqZCTFrG58KwYxLYP6fYPNjzCCNgeNBdcwbw"
GRAPH_URL = "https://graph.facebook.com/v19.0"
INSTAGRAM_ID = "72855597595"
