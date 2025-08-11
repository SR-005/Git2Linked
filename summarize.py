import os
from dotenv import load_dotenv
import google.generativeai as genai

#Load and Read API Ket from .env file and configure Gemini SDK
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#setting up gemini model
model = genai.GenerativeModel("gemini-1.5-flash") 
chat = model.start_chat(history=[])

#API Fetch Function
def main(content):
    print("-------------content recieved-------------")
    prompt = f"Summarize the following GitHub README in under 100 words for a LinkedIn post:\n\n{content}"
    try:
        response=model.generate_content(prompt)
        return response.text
        ''', chat.history'''
    except Exception as e:
        return f"Error: {e}"