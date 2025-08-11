from flask import Flask,request
import requests
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID= os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"

app=Flask(__name__)
@app.route("/callback")

def callback():
    code = request.args.get("code")
    if not code:
        return "Error: no code provided"

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=token_data, headers=token_headers)
    if response.status_code != 200:
        return f"Error getting token: {response.text}"

    access_token = response.json().get("access_token")
    return f"Access Token: {access_token}"

@app.route("/",methods=["GET", "POST"])

def index():
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope=w_member_social"
    )
    return f'<a href="{auth_url}">Login with LinkedIn</a>'

if __name__=="__main__":
    app.run(debug=True)