# 🔗 Insta Auto Link Bot (Render Ready)

A simple Flask server that listens to Instagram post comments via Webhook and sends product links via DM. Firebase used for mapping `post_id` → `product URL`.

## 🚀 Features
- Firebase real-time DB integration
- Auto-replies when someone comments "link"
- Flask + Gunicorn server for deployment on Render

## 🧾 Endpoints

### `/`  
Basic health check.  

### `/save_mapping`  
```json
POST
{
  "post_id": "1234567890",
  "link": "https://yourstore.com/product1"
}
