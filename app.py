from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Load from environment or local fallback
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/clothingDB")
client = MongoClient(MONGO_URI)
db = client["clothingDB"]
collection = db["clothes"] 

@app.route("/categories", methods=["GET"])
def get_categories():
    categories = collection.distinct("category")
    return jsonify({"categories": [cat.lower() for cat in categories]})

@app.route("/category/<category_name>", methods=["GET"])
def get_items_by_category(category_name):
    items = list(collection.find({"category": {"$regex": category_name, "$options": "i"}}, {"_id": 0}))
    return jsonify(items) if items else jsonify({"message": "No items found"}), 200

@app.route("/search", methods=["GET"])
def search_items():
    query = request.args.get("query", "").lower()
    if not query:
        return jsonify({"message": "Please provide a search query"}), 400

    items = list(collection.find(
        {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }, {"_id": 0}
    ))
    return jsonify(items) if items else jsonify({"message": "No matching items found"}), 200

@app.route("/add", methods=["POST"])
def add_item():
    data = request.get_json()
    collection.insert_one(data)
    return jsonify({"message": "Item added successfully"}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
