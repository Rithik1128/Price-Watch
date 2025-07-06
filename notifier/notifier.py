import pymongo
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

cluster = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = cluster["pricewatch"]
collection = db["products"]

def send_email_notification(recipient_email, product_name, current_price, target_price):
    """Send email notification when target price is reached"""
    try:
        # Email configuration from environment variables
        sender_email = os.getenv('EMAIL_SENDER')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = f"Price Alert: {product_name}"
        
        # Email body
        body = f"""
        Great news! The price for {product_name} has dropped!
        
        Current Price: ₹{current_price}
        Target Price: ₹{target_price}
        
        Time to buy!
        """
        
        message.attach(MIMEText(body, "plain"))
        
        # Gmail SMTP configuration
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✅ Email sent to {recipient_email} for {product_name}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def check_price_alerts():
    """Check all products and send notifications if current price <= target price"""
    try:
        products = collection.find({})
        
        for product in products:
            # Get fields from your actual MongoDB document structure
            price_str = product.get('price')
            target_price_str = product.get('target price')
            email = product.get('email')
            product_name = product.get('product_name', 'Unknown Product')
            
            # Parse prices - extract numeric values from strings like "₹17,790.00"
            try:
                if price_str and target_price_str and email:
                    # Extract numeric value from price string
                    current_price = float(price_str.replace('Deal Price\n₹', '').replace(',', ''))
                    target_price = float(target_price_str.replace('₹', '').replace(',', ''))
                    
                    if current_price <= target_price:
                        print(f"🎯 Target price reached for {product_name}")
                        send_email_notification(email, product_name, current_price, target_price)
                    else:
                        print(f"💰 {product_name}: Current ₹{current_price} > Target ₹{target_price}")
                else:
                    print(f"⚠️ Missing data for product: {product.get('_id')}")
            except (ValueError, AttributeError) as e:
                print(f"❌ Error parsing price for {product_name}: {e}")
                
    except Exception as e:
        print(f"❌ Error checking price alerts: {e}")

if __name__ == "__main__":
    print("🚀 Starting Price Alert Check")
    print("=" * 50)
    check_price_alerts()
    cluster.close()
