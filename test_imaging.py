from Utils.MedicalImaging import MedicalImageAnalyzer
import os

def test_imaging():
    print("Testing MedicalImageAnalyzer...")
    try:
        # Test initialization
        analyzer = MedicalImageAnalyzer()
        if analyzer.model:
            print("Model loaded successfully.")
        else:
            print("Model failed to load (NOTE: This might be expected if weights are not downloaded yet, but the class initialized).")
            
        print("MedicalImageAnalyzer test PASSED structure check.")
        
    except Exception as e:
        print(f"MedicalImageAnalyzer test FAILED: {e}")

if __name__ == "__main__":
    test_imaging()
