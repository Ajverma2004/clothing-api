
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from pymongo import MongoClient
from bson import ObjectId
import os

app = FastAPI()

# MongoDB connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/clothingDB")
client = MongoClient(MONGO_URI)
db = client["clothingDB"]
collection = db["clothes"]
banner_collection = db["banners"]

# Pydantic models for validation
class Item(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]

class Banner(BaseModel):
    category: str
    banner_url: str

# Helper to convert MongoDB ObjectId to str
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/products")
async def get_all_products():
    products = [serialize_doc(p) for p in collection.find()]
    return JSONResponse(content=products)

@app.get("/product/{product_id}")
async def get_product_by_id(product_id: str):
    try:
        product = collection.find_one({"_id": ObjectId(product_id)})
        if product:
            return JSONResponse(content=serialize_doc(product))
        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid product ID: {e}")

@app.get("/categories")
async def get_categories():
    categories = collection.distinct("category")
    return {"categories": [cat.lower() for cat in categories]}

@app.get("/category/{category_name}")
async def get_items_by_category(category_name: str):
    items = list(collection.find({"category": {"$regex": category_name, "$options": "i"}}))
    if items:
        return [serialize_doc(item) for item in items]
    return {"message": "No items found"}

@app.get("/search")
async def search_items(query: str = ""):
    if not query:
        raise HTTPException(status_code=400, detail="Please provide a search query")
    items = list(collection.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}}
        ]
    }))
    return [serialize_doc(item) for item in items]

@app.post("/add")
async def add_item(item: Item):
    collection.insert_one(item.dict())
    return {"message": "Item added successfully"}

@app.get("/banners")
async def get_banners():
    banners = list(banner_collection.find({}, {"_id": 0}))
    return banners

@app.post("/banners")
async def add_banner(banner: Banner):
    existing = banner_collection.find_one({"category": banner.category})
    if existing:
        raise HTTPException(status_code=409, detail=f"Banner for category '{banner.category}' already exists.")
    banner_collection.insert_one(banner.dict())
    return {"message": "Banner added successfully"}
