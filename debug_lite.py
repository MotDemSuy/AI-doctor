from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import time

load_dotenv('apikey.env')

def test_lite():
    print("Testing gemini-2.0-flash-lite-001...")
    try:
        model = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.0-flash-lite-001")
        start = time.time()
        res = model.invoke("Hello, are you working?")
        print(f"Success! Time: {time.time()-start:.2f}s")
        print(res.content)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_lite()
