from flask import Flask, request, redirect, url_for, session
import requests
from dotenv import load_dotenv
import os

# Load sensitive information from .env
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    # Request all needed scopes
    scope = "openid profile email w_member_social"
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scope.replace(' ', '%20')}"
    )
    return f'<a href="{auth_url}">Login with LinkedIn</a>'


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: no code provided"

    # Exchange code for access token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=token_data, headers=token_headers)
    if response.status_code == 200:
        token_json = response.json()
        access_token = token_json.get("access_token")
        session["access_token"] = access_token
        return redirect(url_for('post'))
    else:
        return f"Failed to get access token: {response.text}"


@app.route("/post")
def post():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("index"))

    headers = {"Authorization": f"Bearer {access_token}","X-Restli-Protocol-Version": "2.0.0"}

    # Get user profile via OpenID endpoint
    me_url = "https://api.linkedin.com/v2/userinfo"
    response = requests.get(me_url, headers=headers)
    if response.status_code != 200:
        return f"Error getting user info: {response.text}"

    userdata = response.json()
    user_sub = userdata.get("sub")  # OpenID returns "sub" instead of "id"
    authorurn = f"urn:li:person:{user_sub}"

    # Prepare post payload
    post_text = "Hello from my Flask app!"
    payload = {"author": authorurn,"lifecycleState": "PUBLISHED","specificContent": {
            "com.linkedin.ugc.ShareContent": {"shareCommentary": {"text": post_text},"shareMediaCategory": "NONE" }},
            "visibility": { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}}

    #Proxy Posting
    print("✅ Post payload prepared (simulation only):")
    print(payload)
    print("✅ Post created successfully (SIMULATION) — No data sent to LinkedIn.")
    
    # Actual Posting
'''    post_url = "https://api.linkedin.com/v2/ugcPosts"
    post_response = requests.post(post_url, headers={**headers, "Content-Type": "application/json"}, json=payload)
    if post_response.status_code == 201:
        print("✅ Post created successfully")
    else:
        print(f"❌ Failed to create post: {post_response.text}")'''

if __name__ == "__main__":
    app.run(debug=True)
