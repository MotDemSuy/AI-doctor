from langchain_ollama import ChatOllama
import time

def test_model(model_name):
    print(f"\nTesting model: '{model_name}'...")
    try:
        model = ChatOllama(model=model_name)
        start = time.time()
        model.invoke("Hi")
        duration = time.time() - start
        print(f"SUCCESS! ({duration:.2f}s)")
        return True
    except Exception as e:
        print(f"FAILED. Error: {e}")
        return False

def main():
    print("--- OLLAMA ID CHECK ---")
    
    m1 = test_model("llama3:8b")
    # m2 = test_model("meditron:7b") # Removed per user request
    
    if m1: # and m2:
        print("\nAll systems GO! You are ready to use the medical app.")
    else:
        print("\nWARNING: Some models are missing.")
        print("Please run the 'ollama pull' commands for the missing models.")

if __name__ == "__main__":
    main()
