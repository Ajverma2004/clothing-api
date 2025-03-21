from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# ✅ Load clothing data from the JSON file
with open("clothing_data.json", "r") as f:
    clothing_data = json.load(f)

@app.route("/categories", methods=["GET"])
def get_categories():
    categories = list(set(item["category"].lower() for item in clothing_data))
    return jsonify({"categories": categories})

@app.route("/category/<category_name>", methods=["GET"])
def get_items_by_category(category_name):
    items = [item for item in clothing_data if item["category"].lower() == category_name.lower()]
    return jsonify(items) if items else jsonify({"message": "No items found"}), 200

@app.route("/search", methods=["GET"])
def search_items():
    query = request.args.get("query", "").lower()
    print(f"Received search query: {query}")

    if not query:
        return jsonify({"message": "Please provide a search query"}), 400

    results = [
        item for item in clothing_data
        if any(word in item["name"].lower() or word in item["description"].lower() for word in query.split())
    ]

    print(f"Matching items: {results}")

    return jsonify(results) if results else jsonify({"message": "No matching items found"}), 200

if __name__ == "__main__":
    app.run(debug=True)
