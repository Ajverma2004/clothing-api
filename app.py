from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

app = Flask(__name__)

# Load from environment or local fallback
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/clothingDB")
client = MongoClient(MONGO_URI)
db = client["clothingDB"]
collection = db["clothes"] 
banner_collection = db["banners"]

@app.route("/products", methods=["GET"])
def get_all_products():
    products = []
    for product in collection.find():
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
        products.append(product)
    return jsonify(products), 200

@app.route("/product/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product = collection.find_one({"_id": ObjectId(product_id)})
        if product:
            product["_id"] = str(product["_id"])
            return jsonify(product), 200
        else:
            return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        return jsonify({"message": "Invalid product ID", "error": str(e)}), 400


@app.route("/categories", methods=["GET"])
def get_categories():
    categories = collection.distinct("category")
    return jsonify({"categories": [cat.lower() for cat in categories]})

@app.route("/category/<category_name>", methods=["GET"])
def get_items_by_category(category_name):
    items = list(collection.find({"category": {"$regex": category_name, "$options": "i"}}))
    
    for item in items:
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
    
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
    return jsonify(items), 200

@app.route("/add", methods=["POST"])
def add_item():
    data = request.get_json()
    collection.insert_one(data)
    return jsonify({"message": "Item added successfully"}), 201



@app.route("/banners", methods=["GET"])
def get_banners():
    banners = list(banner_collection.find({}, {"_id": 0}))
    return jsonify(banners), 200

@app.route("/banners", methods=["POST"])
def add_banner():
    data = request.get_json()
    
    # Basic validation
    if not data or "category" not in data or "banner_url" not in data:
        return jsonify({"message": "Both 'category' and 'banner_url' are required."}), 400

    # Optional: Check if a banner for this category already exists
    existing = banner_collection.find_one({"category": data["category"]})
    if existing:
        return jsonify({"message": f"Banner for category '{data['category']}' already exists."}), 409

    # Insert the banner
    banner_collection.insert_one({
        "category": data["category"],
        "banner_url": data["banner_url"]
    })

    return jsonify({"message": "Banner added successfully."}), 201



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
