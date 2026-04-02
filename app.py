from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# --- MONGODB ATLAS CONNECTION ---
uri = "mongodb+srv://jujawalid_db_user:Juja2004@ecohomear.dj1aeau.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    db = client.EcohomeAr 
    collection = db.appliances
    client.admin.command('ping')
    print("✅ DATABASE CONNECTED: MongoDB Atlas is Live")
except Exception as e:
    print(f"❌ DATABASE ERROR: {e}")

@app.route('/')
def home():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    appliance_id = data.get('id')
    appliance = collection.find_one({"id": appliance_id})
    
    if appliance:
        watts = appliance['watts']
        # DEWA Pricing: ~0.38 for High Slab (AC), ~0.23 for Low Slab (LED/Fridge)
        rate = 0.38 if watts > 2000 else 0.23
        cost_per_hour = (watts / 1000) * rate

        # Logic for Nudges and Sustainability Recommendations
        if watts > 2000:
            color, nudge = "red", "⚠️ CRITICAL: HIGH COST"
            tip = "Recommendation: Set AC to 24°C. Each degree higher saves 6% on your DEWA bill."
        elif watts > 100:
            color, nudge = "yellow", "⚡ MODERATE: STABLE"
            tip = "Sustainability: Ensure fridge coils are clean. Dust increases consumption by 15%."
        else:
            color, nudge = "green", "✅ EFFICIENT: OPTIMAL"
            tip = "Eco-Tip: LED bulbs use 80% less energy than old halogen bulbs. Great choice!"

        return jsonify({
            "name": appliance['name'],
            "watts": watts,
            "cost": f"{cost_per_hour:.3f}",
            "color": color,
            "nudge": nudge,
            "tip": tip
        })
    return jsonify({"error": "Appliance not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)