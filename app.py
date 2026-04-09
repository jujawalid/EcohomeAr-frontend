from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# --- DATABASE CONNECTION ---
uri = "mongodb+srv://jujawalid_db_user:Juja2004@ecohomear.dj1aeau.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client.EcohomeAr 
    collection = db.appliances
    client.admin.command('ping')
    print("\n✅ MONGODB CONNECTED SUCCESSFULLY")
except Exception as e:
    print(f"\n❌ DATABASE ERROR: {e}")

@app.route('/')
def home():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    appliance_id = data.get('id')
    # EDIT: Capture the Guest Name from the frontend
    user_name = data.get('userName', 'Guest') 
    
    appliance = collection.find_one({"id": appliance_id})
    
    if appliance:
        watts = appliance['watts']
        # Professional DEWA-style slab logic
        rate = 0.38 if watts > 2000 else 0.23
        cost_per_hour = (watts / 1000) * rate

        # --- EDIT: PERSONALIZED RECOMMENDATION ENGINE ---
        if watts > 2000:
            color, nudge = "red", " HIGH CONSUMPTION"
            # Personalized tip using the Guest Name
            tip = f"Hey {user_name}, setting AC to 24°C can save you AED 50/month."
            percentage_height = 90  # For your frontend chart
        elif watts > 100:
            color, nudge = "yellow", " MODERATE USAGE"
            tip = "Recommendation: Keep Fridge 10cm from walls for 15% better airflow."
            percentage_height = 40
        else:
            color, nudge = "green", "HIGHLY EFFICIENT"
            tip = f"Eco-Tip: {user_name}, your LED is 100% compatible with Solar Energy."
            percentage_height = 10

        return jsonify({
            "name": appliance['name'],
            "watts": watts,
            "cost": f"{cost_per_hour:.3f}",
            "color": color,
            "nudge": nudge,
            "tip": tip,
            "chartHeight": percentage_height, # Used for the CSS Bar Chart
            "userName": user_name
        })
    
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)