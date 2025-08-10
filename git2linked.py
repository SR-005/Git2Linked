import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")

headers = {"Authorization": f"token {TOKEN}"}

repourl = f"https://api.github.com/users/{USERNAME}/repos"
reporesponse = requests.get(repourl, headers=headers)
repos = reporesponse.json()

print("\n-----------Your Repositories-----------")
for index, repo in enumerate(repos, 1):
    print(f"{index}. {repo['name']}")

choice = int(input("\nEnter repo number to fetch README: ")) - 1
reponame = repos[choice]["name"]

readme_url = f"https://api.github.com/repos/{USERNAME}/{reponame}/readme"
readmeresponse = requests.get(readme_url, headers=headers)
readmedata = readmeresponse.json()

if "content" in readmedata:
    content = base64.b64decode(readmedata["content"]).decode("utf-8")
    print("\n=== README.md ===\n")
    print(content)
else:
    print("No README found for this repository.")