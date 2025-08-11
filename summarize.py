import os
from dotenv import load_dotenv
import google.generativeai as genai

#Load and Read API Ket from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

#configure Gemini SDK
genai.configure(api_key=api_key)
#setting up gemini model
model = genai.GenerativeModel("gemini-1.5-flash") 
chat = model.start_chat(history=[])

#API Fetch Function
def main(userinput):
    try:
        response = chat.send_message(userinput)
        return response.text, chat.history
    except Exception as e:
        return f"Error: {e}"