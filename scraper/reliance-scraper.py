from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


# ----- CONFIG -----
PRODUCT_URL = "https://www.reliancedigital.in/product/lg-7-kg-top-loading-fully-automatic-washing-machine-t70spsf2z"
CSV_FILE = "../price_history.csv"
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
if not MONGO_CONNECTION_STRING:
    raise ValueError("No MONGO_CONNECTION_STRING found in environment variables. Please set it before running the script.")


MONGO_DB_NAME = "pricewatch"
MONGO_COLLECTION_NAME = "products"


# ------------------

def init_browser():
    options = Options()
    options.add_argument("--headless")  # Uncomment if you want it headless
    options.add_argument("--start-maximized")
    service = Service()
    return webdriver.Chrome(service=service, options=options)

def get_price(driver):
    driver.get(PRODUCT_URL)
    print("[INFO] Navigated to product page, waiting for it to load...")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-price"))
        )
        price_element = driver.find_element(By.CLASS_NAME, "product-price")
        return price_element.text.strip()
    except Exception as e:
        print("[ERROR] Could not get price:", e)
        return None

def get_product_title(driver):
    try:
        return driver.title.split("|")[0].strip()
    except:
        return "Unknown Product"

def log_price_to_mongodb(product_name, price):
    """Logs the product name and price to MongoDB."""
    try:
        client = MongoClient(MONGO_CONNECTION_STRING)
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
        if 'client' in locals() and client:
            client.close()

def log_price(product_name, price):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Time", "Product", "Price"])
        writer.writerow([now, product_name, price])

    print(f"[LOG] {now} | {product_name} | {price}")

def main():
    print(">> Starting Price Watcher")
    browser = init_browser()

    try:
        price = get_price(browser)
        if price:
            print(f"✅ PRICE FOUND: {price}")
            product_name = get_product_title(browser)
            log_price(product_name, price)
            log_price_to_mongodb(product_name, price)
        else:
            print("[FAIL] Price not found.")
    finally:
        browser.quit()
        print("[INFO] Browser closed.")

if __name__ == "__main__":
    main()