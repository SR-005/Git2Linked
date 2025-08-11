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

    while(1):
        print("Which type of description do yoou want in for you project: ")
        print("1. Professional – Bullet Points & Technical\n2. Friendly & Casual\n3. Engaging & Persuasive\n4. Technical-Focused\n5.Custom")
        promptnumber=int(input("Choose your style: "))
        
        if promptnumber==1:
            prompt="You are writing a professional LinkedIn post targeted at recruiters and industry peers. Summarize the provided GitHub README in a concise, clear, and formal tone. Highlight the most important features, functions, and achievements in bullet points. Focus on technical details, measurable outcomes, and skills demonstrated. Avoid casual language, slang, or jokes. Keep it between 80–150 words."
            break
        elif promptnumber==2:
            prompt="You are creating a friendly and approachable LinkedIn post to showcase a GitHub project. Start with a light, clever, or mildly humorous opening line to grab attention (but keep it professional enough for LinkedIn). Use conversational language, everyday words, and a warm tone. Briefly explain the purpose and main features of the project in 3–5 short sentences. Make it sound like you are telling a friend about your project. End with an inviting line encouraging people to check out the repo."
            break
        elif promptnumber==3:
            prompt="You are creating a persuasive LinkedIn post to make people want to check out the GitHub repository. Hook the reader in the first sentence by emphasizing the problem this project solves or the value it brings. Highlight unique selling points, benefits, or innovative elements of the project. Use clear and confident language that inspires curiosity and action. End with a call-to-action, such as “Explore the code here” or “Let’s collaborate!” Limit to 100–150 words."
            break
        elif promptnumber==4:
            prompt="You are creating a LinkedIn post for a technical audience, such as developers and engineers. Focus heavily on the architecture, tools, frameworks, algorithms, and technical challenges solved in the project. Use precise terminology and describe the core technologies and workflows. Assume the reader understands technical jargon, but still keep the explanation structured and easy to follow. Avoid fluff — prioritize technical depth over marketing language."
            break
        elif promptnumber==5:
            prompt=input("Describe the style of description you want: ")
            break
        else:
            print("Enter a valid option")

    prompt=prompt+f" Github Readme Content is given below \n\n{content}"
    linkedinfeed=summarizereadme(prompt)
    print("\n=======LinkedIn-Friendly Summary=======\n")
    print(linkedinfeed)
else:
    print("No README found for this repository.")
