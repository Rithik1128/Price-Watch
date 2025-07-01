from pymongo import MongoClient
import certifi  # for TLS CA certificates

# Replace <db_password> with your actual password
DB_PASSWORD = "pricewatch599#"  # TODO: Replace with your real password
CONNECTION_STRING = f"mongodb+srv://pricewatch:{DB_PASSWORD}@pricewatch.mddfv3l.mongodb.net/?retryWrites=true&w=majority&appName=pricewatch"

client = MongoClient(
    CONNECTION_STRING,
    tls=True,
    tlsCAFile=certifi.where()
)

# Example: Access a database (replace 'your_database_name' with the actual name)
db = client['pricewatch']  # TODO: Replace with your actual database name``