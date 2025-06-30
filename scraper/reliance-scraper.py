from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import re

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from mongo_data.mongo_connect import db

url = input("Enter the product URL: ")

# ----- CONFIG -----
PRODUCT_URL = url


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

def extract_numeric_price(price_str):
    # Extract the first number (with optional commas and decimals)
    match = re.search(r'[\d,]+(?:\.\d+)?', price_str.replace('\n', ''))
    if match:
        # Remove commas and convert to int (ignore decimals)
        return int(float(match.group(0).replace(',', '')))
    raise ValueError(f"Could not extract numeric price from: {price_str}")

def log_price_to_mongo(product_name, price, product_url):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    numeric_price = extract_numeric_price(price)
    product_doc = {
        "user_id": None,  # Set this if you have user context
        "product_url": product_url,
        "title": product_name,
        "initial_price": numeric_price,
        "tracking_mode": "below",  # Default, can be changed
        "target_price": None,  # Set this if you have a target
        "current_price": numeric_price,
        "last_notified_price": None,
        "scraped_at": now
    }
    db.products.insert_one(product_doc)
    print(f"[MONGO] Inserted: {product_doc}")


def main():
    print(">> Starting Price Watcher")
    browser = init_browser()

    try:
        price = get_price(browser)
        if price:
            print(f"✅ PRICE FOUND: {price}")
            product_name = get_product_title(browser)
            log_price_to_mongo(product_name, price, PRODUCT_URL)
        else:
            print("[FAIL] Price not found.")
    finally:
        browser.quit()
        print("[INFO] Browser closed.")

if __name__ == "__main__":
    main()