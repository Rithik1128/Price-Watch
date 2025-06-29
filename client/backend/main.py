from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Middleware to handle sessions
app.add_middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])

# CORS config for React frontend (Vite default port: 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    user = await oauth.google.get("userinfo", token=token)
    user_data = user.json()

    request.session["user"] = user_data
    return RedirectResponse(url="http://localhost:5173/dashboard")


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
