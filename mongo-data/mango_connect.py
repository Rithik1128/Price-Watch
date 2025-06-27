
from pymongo import MongoClient

# Replace <db_password> with your actual password
DB_PASSWORD = "pricewatch599#"  # TODO: Replace with your real password
CONNECTION_STRING = f"mongodb+srv://pricewatch:{DB_PASSWORD}@pricewatch.mddfv3l.mongodb.net/"

client = MongoClient(CONNECTION_STRING)

# Example: Access a database (replace 'your_database_name' with the actual name)
db = client['pricewatch']  # TODO: Replace with your actual database name

# You can now use 'db' to interact with your MongoDB collections
