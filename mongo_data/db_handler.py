import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Explicitly load the .env file from the project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = "pricewatch"
MONGO_PRODUCTS_COLLECTION_NAME = "products" # For scraper logs
MONGO_TRACKED_PRODUCTS_COLLECTION_NAME = "tracked_products" # For user-tracked products


if not MONGO_CONNECTION_STRING:
    raise ValueError("No MONGO_CONNECTION_STRING found in environment variables.")

def get_db_client():
    """Returns a MongoDB client object."""
    return MongoClient(MONGO_CONNECTION_STRING)

def add_product_for_user(user_id, product_url):
    """Adds a new product URL for a user to track."""
    client = None
    try:
        client = get_db_client()
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_TRACKED_PRODUCTS_COLLECTION_NAME]

        # Avoid adding duplicate URLs for the same user
        existing_product = collection.find_one({"user_id": user_id, "product_url": product_url})
        if existing_product:
            print(f"[INFO] User {user_id} is already tracking {product_url}.")
            return {"status": "exists", "product_id": existing_product["_id"]}

        document = {
            "user_id": user_id,
            "product_url": product_url,
            "product_name": "Fetching...", # Placeholder name
            "current_price": None,
            "price_history": [],
            "created_at": datetime.now()
        }
        
        result = collection.insert_one(document)
        print(f"[INFO] Added product {product_url} for user {user_id}.")
        return {"status": "added", "product_id": result.inserted_id}
        
    except Exception as e:
        print(f"[ERROR] Could not add product for user: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        if client:
            client.close()

def get_products_for_user(user_id):
    """Retrieves all tracked products for a given user."""
    client = None
    try:
        client = get_db_client()
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_TRACKED_PRODUCTS_COLLECTION_NAME]
        
        products = list(collection.find({"user_id": user_id}))
        
        # Convert ObjectId to string for JSON serialization
        for product in products:
            product["_id"] = str(product["_id"])
            
        return products
        
    except Exception as e:
        print(f"[ERROR] Could not retrieve products for user {user_id}: {e}")
        return []
    finally:
        if client:
            client.close()

def log_price_to_mongodb(product_name, price):
    """Logs the product name and price to MongoDB."""
    client = None  # Initialize client to None
    try:
        client = get_db_client()
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_PRODUCTS_COLLECTION_NAME]
        
        document = {
            "product_name": product_name,
            "price": price,
            "timestamp": datetime.now()
        }
        
        collection.insert_one(document)
        print("[INFO] Logged price to MongoDB.")
        
    except Exception as e:
        print(f"[ERROR] Could not log price to MongoDB: {e}")
    finally:
        if client:
            client.close()
