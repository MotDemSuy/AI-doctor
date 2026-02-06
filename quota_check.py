from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import time
import os

load_dotenv('apikey.env')

MODELS = [
    "gemini-2.0-flash", 
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite-001",
    "gemini-flash-latest",
    "gemini-1.5-flash"
]

def check_quota():
    print("--- QUOTA DIAGNOSTIC ---")
    print(f"Testing {len(MODELS)} models to find one with available quota.\n")
    
    available_model = None
    
    for model_name in MODELS:
        print(f"Testing: {model_name} ... ", end="", flush=True)
        try:
            llm = ChatGoogleGenerativeAI(temperature=0, model=model_name)
            # Try a very simple prompt
            start = time.time()
            llm.invoke("Hi")
            duration = time.time() - start
            print(f"OK! ({duration:.2f}s)")
            available_model = model_name
            # If we found one, we could stop, but let's check all to give a full report
            # unless we want to save quota? Let's stop at the first success to be safe.
            print(f">>> FOUND WORKING MODEL: {model_name}")
            return
            
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print("RATE LIMITED (Shared Quota)")
            elif "404" in str(e) or "NOT_FOUND" in str(e):
                print("NOT FOUND")
            else:
                print(f"ERROR: {str(e)[:50]}...")
    
    print("\nCONCLUSION: All models are Rate Limited or Unavailable.")
    print("Reason: Google Free Tier API keys likely share a single global quota (RPM) across all models.")

if __name__ == "__main__":
    check_quota()
