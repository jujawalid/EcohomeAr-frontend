from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

uri = "mongodb+srv://jujawalid_db_user:Juja2004@ecohomear.dj1aeau.mongodb.net/?retryWrites=true&w=majority"

# --- CONNECT TO DATABASE ---
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client.EcohomeAr 
    collection = db.appliances
    
    # The 'ping' check
    client.admin.command('ping')
    print("\n" + "="*30)
    print("✅ MONGODB CONNECTED SUCCESSFULLY")
    print(f"📡 Using Collection: {collection.name}")
    print("="*30 + "\n")
except Exception as e:
    print("\n" + "!"*30)
    print(f"❌ DATABASE ERROR: {e}")
    print("!"*30 + "\n")

@app.route('/')
def home():
    # This works regardless of which folder you run the command from
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    appliance_id = data.get('id')
    appliance = collection.find_one({"id": appliance_id})
    
    if appliance:
        watts = appliance['watts']
        rate = 0.38 if watts > 2000 else 0.23
        cost_per_hour = (watts / 1000) * rate

        if watts > 2000:
            color, nudge = "red", " HIGH CONSUMPTION"
            tip = "Recommendation: Set AC to 24°C to optimize cooling efficiency."
        elif watts > 100:
            color, nudge = "yellow", " MODERATE USAGE"
            tip = "Sustainability: Keep appliances 10cm from walls for better airflow."
        else:
            color, nudge = "green", "HIGHLY EFFICIENT"
            tip = "Eco-Tip: LED lighting reduces energy waste by 80%."

        return jsonify({
            "name": appliance['name'],
            "watts": watts,
            "cost": f"{cost_per_hour:.3f}",
            "color": color,
            "nudge": nudge,
            "tip": tip
        })
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)