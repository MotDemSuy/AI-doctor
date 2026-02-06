import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path='apikey.env')
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in apikey.env")
else:
    print(f"Using API Key: {api_key[:5]}...")
    genai.configure(api_key=api_key)
    print("Listing available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error: {e}")
