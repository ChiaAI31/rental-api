from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Scoring dictionaries
furnishing_score = {
    "Unfurnished": 0,
    "Partially Furnished": 150,
    "Fully Furnished": 300
}

floor_score = {
    "Low Floor": 0,
    "Mid Floor": 100,
    "High Floor": 200
}

tag_score = {
    "Sea View": 150,
    "Corner Unit": 100,
    "Near MRT": 180
}

@app.route('/')
def health():
    return '✅ Backend is running on Railway.'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # Calculate base and additional scores
        base_price = 2100
        total = base_price
        total += furnishing_score.get(data.get("furnishing"), 0)
        total += floor_score.get(data.get("floorLevel"), 0)
        total += tag_score.get(data.get("boostTags"), 0)

        if data.get("rentFasterBoost"):
            total -= 80  # small discount

        return jsonify({ "predictedPrice": round(total, 2) })
    
    except Exception as e:
        return jsonify({ "error": str(e) }), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
