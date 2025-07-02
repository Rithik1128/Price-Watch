from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongo_data.db_handler import log_price_to_mongodb


# ----- CONFIG -----
PRODUCT_URL = "https://www.reliancedigital.in/product/lg-7-kg-top-loading-fully-automatic-washing-machine-t70spsf2z"


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

def main():
    print(">> Starting Price Watcher")
    browser = init_browser()

    try:
        price = get_price(browser)
        if price:
            print(f"✅ PRICE FOUND: {price}")
            product_name = get_product_title(browser)
            log_price_to_mongodb(product_name, price)
        else:
            print("[FAIL] Price not found.")
    finally:
        browser.quit()
        print("[INFO] Browser closed.")

if __name__ == "__main__":
    main()