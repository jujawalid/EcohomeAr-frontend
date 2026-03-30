from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# --- MONGODB ATLAS CONNECTION ---
uri = "mongodb+srv://jujawalid_db_user:Juja2004@ecohomear.dj1aeau.mongodb.net/?retryWrites=true&w=majority"

try:
    # Increased timeout for cloud-to-cloud connection
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    db = client.EcohomeAr 
    collection = db.appliances
    # Test connection
    client.admin.command('ping')
    print("✅ DATABASE CONNECTED: MongoDB Atlas is Live")
except Exception as e:
    print(f"❌ DATABASE ERROR: {e}")

@app.route('/')
def home():
    # Serving index.html from the same directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    appliance_id = data.get('id')
    
    appliance = collection.find_one({"id": appliance_id})
    
    if appliance:
        watts = appliance['watts']
        
        # --- DYNAMIC NUDGE LOGIC ---
        if watts > 2000: # Old Window AC (2800W)
            color = "red"
            nudge = "⚠️ CRITICAL: High DEWA Slab 3"
        elif watts > 100: # Fridge (450W)
            color = "yellow"
            nudge = "⚡ MODERATE: Essential Load"
        else: # LED Bulb (12W)
            color = "green"
            nudge = "✅ EFFICIENT: Low Impact"

        return jsonify({
            "name": appliance['name'],
            "watts": watts,
            "color": color,
            "nudge": nudge
        })
    return jsonify({"error": "Appliance not found"}), 404

if __name__ == '__main__':
    # CRITICAL FOR RENDER: 
    # Render assigns a random port; this line grabs it automatically.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)