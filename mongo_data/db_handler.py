import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Explicitly load the .env file from the project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = "pricewatch"
MONGO_COLLECTION_NAME = "products"

if not MONGO_CONNECTION_STRING:
    raise ValueError("No MONGO_CONNECTION_STRING found in environment variables.")

def get_db_client():
    """Returns a MongoDB client object."""
    return MongoClient(MONGO_CONNECTION_STRING)

def log_price_to_mongodb(product_name, price):
    """Logs the product name and price to MongoDB."""
    client = None  # Initialize client to None
    try:
        client = get_db_client()
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION_NAME]
        
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
