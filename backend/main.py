from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import json
import httpx
from urllib.parse import urlencode, quote

from .config import (
    GOOGLE_AUTH_URL,
    GOOGLE_TOKEN_URL,
    GOOGLE_USERINFO_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    REDIRECT_URI,
    FRONTEND_URL,
)

app = FastAPI(title="Proactive API", description="Google OAuth server for Proactive")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"message": "Proactive Auth Backend API is running"}


@app.get("/api/auth/google/login")
def google_login():
    """
    Step 1 of OAuth 2.0 Flow:
    Redirects the user to Google's OAuth 2.0 consent page.
    """
    if not GOOGLE_CLIENT_ID or GOOGLE_CLIENT_ID == "your_google_client_id_here":
        raise HTTPException(
            status_code=400,
            detail="GOOGLE_CLIENT_ID is not configured in backend environment (.env)."
        )

    # Scopes for basic profile and email access
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url=url)


@app.get("/api/auth/google/callback")
async def google_callback(code: str = Query(...)):
    """
    Step 2 of OAuth 2.0 Flow:
    Google redirects back to this endpoint with an authorization code.
    Exchanges the code for tokens and retrieves user profile details.
    """
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=400, detail="OAuth credentials missing in server config.")

    # Request payload to exchange authorization code for access token
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        # Exchange authorization code for access token
        token_response = await client.post(GOOGLE_TOKEN_URL, data=token_data)
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve token from Google.")
        
        tokens = token_response.json()
        access_token = tokens.get("access_token")

        # Fetch user info using the access token
        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        if userinfo_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info from Google.")

        user_profile = userinfo_response.json()

    # Convert dictionary to JSON string and URL quote it for frontend consumption
    json_str = json.dumps(user_profile)
    frontend_redirect_url = f"{FRONTEND_URL}?user={quote(json_str)}"
    return RedirectResponse(url=frontend_redirect_url)
