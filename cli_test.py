import time
from Utils.Agents import Generalist
from dotenv import load_dotenv
import os

# Load env
load_dotenv('apikey.env')

def main():
    print("--- AI MEDICAL DIAGNOSTICS CLI TEST ---")
    print("Checking environment...")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in apikey.env")
        return

    print("Status: Ready.")
    
    # Sample Input
    patient_report = """
    Họ tên: Test Patient
    Tuổi: 45
    Triệu chứng: Đau thắt ngực trái, lan ra cánh tay trái, vã mồ hôi, buồn nôn. Tiền sử hút thuốc lá.
    """
    
    print(f"\n[Input Report]\n{patient_report}\n")
    print("Running Generalist Agent (Triage)... Please wait (approx 5-10s)")
    
    try:
        start_time = time.time()
        agent = Generalist(patient_report)
        print(f"Model: {agent.model.model}")
        
        result = agent.run()
        end_time = time.time()
        
        print("\n[Result from AI]")
        print(result)
        print(f"\nSuccess! Time taken: {end_time - start_time:.2f}s")
        
    except Exception as e:
        print("\n[ERROR]")
        print(str(e))
        print("Please check your API Key or Internet Connection.")

if __name__ == "__main__":
    main()
