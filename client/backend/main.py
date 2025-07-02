import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))

from fastapi import FastAPI, Request, Depends
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from user_db import add_or_update_user
from mongo_data.db_handler import add_product_for_user, get_products_for_user
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# Middleware to handle sessions
app.add_middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])

# CORS config for React frontend (Vite default port: 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    product_url: str

# Dependency to get the current user from the session
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return None
    return user

# OAuth setup with Authlib (✅ includes api_base_url fix)
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",  # ✅ full config
    client_kwargs={
        "scope": "openid email profile"
    }
)


@app.get("/")
async def home():
    return {"msg": "Backend running."}

@app.get("/login/google")
async def login(request: Request):
    redirect_uri = "http://localhost:8000/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    userinfo_endpoint = oauth.google.server_metadata["userinfo_endpoint"]
    user = await oauth.google.get(userinfo_endpoint, token=token)
    user_data = user.json()

    # Save user data to the database
    add_or_update_user(user_data)

    request.session["user"] = user_data
    return RedirectResponse(url="http://localhost:3000/")


@app.get("/profile")
async def profile(request: Request):
    user = request.session.get("user")
    if not user:
        return {"error": "Not logged in"}
    return user

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return {"message": "Logged out"}

@app.post("/products")
async def track_product(product: Product, user: dict = Depends(get_current_user)):
    if not user:
        return {"error": "Unauthorized"}, 401
    
    user_id = user.get("sub") # Using Google's 'sub' as the unique user ID
    result = add_product_for_user(user_id, product.product_url)
    return result

@app.get("/products")
async def get_tracked_products(user: dict = Depends(get_current_user)):
    if not user:
        return {"error": "Unauthorized"}, 401

    user_id = user.get("sub")
    products = get_products_for_user(user_id)
    return products
