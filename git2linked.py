import requests
import base64           #github readme is based of base64, this is needed dor decoding the info
import google.generativeai as genai
import os
from dotenv import load_dotenv
from summarize import main as summarizereadme

#getting sensitive information from .env file:
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")

headers = {"Authorization": f"token {TOKEN}"}       #setting up http head to send requests

repourl = f"https://api.github.com/users/{USERNAME}/repos"  #building endpoint to users repo
reporesponse = requests.get(repourl, headers=headers)   #fetches the list of repo using API
repos = reporesponse.json()     #converts it into .json packages

#print all the fetched repos:
print("\n-----------Your Repositories-----------")
for index, repo in enumerate(repos, 1):
    print(f"{index}. {repo['name']}")

#prompt the user for the repo number
choice = int(input("\nEnter repo number to fetch README: ")) - 1
reponame = repos[choice]["name"]

readme_url = f"https://api.github.com/repos/{USERNAME}/{reponame}/readme"   #building the endpoint
readmeresponse = requests.get(readme_url, headers=headers)  #fetches the readme content using API
readmedata = readmeresponse.json()      #converts it into .json packages

if "content" in readmedata:
    content = base64.b64decode(readmedata["content"]).decode("utf-8")   #base64.b64decode converts it into raw bytes and decode("utf-8") turns it into normal strings 
    print("\n=== README.md ===\n")
    print(content)

    linkedinfeed=summarizereadme(content)
    print("\n=======LinkedIn-Friendly Summary=======\n")
    print(linkedinfeed)
else:
    print("No README found for this repository.")
