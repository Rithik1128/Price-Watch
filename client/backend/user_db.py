import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env from the project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = "pricewatch"
MONGO_COLLECTION_NAME = "user"

if not MONGO_CONNECTION_STRING:
    raise ValueError("No MONGO_CONNECTION_STRING found in environment variables.")

client = MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

def add_or_update_user(user_data: dict):
    """Finds a user by email and updates their data, or creates a new user."""
    try:
        # Use the user's email as the unique identifier
        query = {"email": user_data.get("email")}
        
        # Prepare the update document
        update = {
            "$set": {
                "name": user_data.get("name"),
                "given_name": user_data.get("given_name"),
                "family_name": user_data.get("family_name"),
                "picture": user_data.get("picture"),
                "locale": user_data.get("locale"),
            },
            "$currentDate": {"last_login": True}
        }
        
        # Perform an "upsert" operation
        # This will update the user if they exist, or insert a new one if they don't.
        collection.update_one(query, update, upsert=True)
        print(f"[INFO] Successfully saved user data for {user_data.get('email')}")
        
    except Exception as e:
        print(f"[ERROR] Could not save user to MongoDB: {e}")
