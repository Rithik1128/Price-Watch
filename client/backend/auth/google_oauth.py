from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# Step 1: Redirect to Google
@router.get("/login")
def login():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["profile", "email"])
    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type="offline", prompt="consent")
    return RedirectResponse(authorization_url)

# Step 2: Google redirects back here
@router.get("/callback")
def callback(request: Request):
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    full_url = str(request.url)
    token = google.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=full_url)

    resp = google.get(USER_INFO_URL)
    user_info = resp.json()
    return {"user": user_info}
