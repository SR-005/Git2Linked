from flask import Flask,request,redirect,url_for,session
import requests
from dotenv import load_dotenv
import os

#loading sensitive informations from .env
load_dotenv()
CLIENT_ID= os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"

app=Flask(__name__)
app.secret_key = os.urandom(24) 

#MAIN PAGE:
@app.route("/",methods=["GET", "POST"])
def index():
    auth_url = ("https://www.linkedin.com/oauth/v2/authorization"f"?response_type=code&client_id={CLIENT_ID}"f"&redirect_uri={REDIRECT_URI}&scope=w_member_social")
    return f'<a href="{auth_url}">Login with LinkedIn</a>'

#OAUTH REDIRECTION
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
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=token_data, headers=token_headers)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        session["access_token"] = access_token
        return redirect(url_for('index'))
    else:
        return "Failed to get access token"

@app.route("/post")
def post():
    accesstoken=session.get("access_token")
    if not accesstoken:
        redirect(url_for("index"))

    headers = {"Authorization": f"Bearer {accesstoken}","X-Restli-Protocol-Version": "2.0.0"}
    url = "https://api.linkedin.com/v2/me"
    response=requests.get(url,headers)
    if response.status_code!=200:
        return f"Error getting user URN: {response.text}"
    
    userdata = response.json()
    userurn = userdata.get("id")
    authorurn = f"urn:li:person:{userurn}"
    
    post_text="Hello"
    payload = {"author": authorurn,"lifecycleState": "PUBLISHED",
            "specificContent": {"com.linkedin.ugc.ShareContent": {"shareCommentary": {"text": post_text},"shareMediaCategory": "NONE"}},
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}}
    
    print(f"✅ Simulated post complete. Payload: {payload}") 
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug=True)