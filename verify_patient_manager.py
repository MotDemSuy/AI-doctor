from Utils.PatientManager import PatientManager
import os
import shutil

def test_patient_manager():
    pm = PatientManager()
    test_cccd = "999999999"
    
    # Clean up before test
    file_path = pm._get_file_path(test_cccd)
    if os.path.exists(file_path):
        os.remove(file_path)

    print("1. Testing Registration...")
    info = {
        "name": "Test User",
        "age": 25,
        "gender": "Nam",
        "height": 180,
        "weight": 75
    }
    pm.save_patient(test_cccd, info)
    
    data = pm.load_patient(test_cccd)
    if data and data['info']['name'] == "Test User":
        print("PASS: Registration")
    else:
        print("FAIL: Registration")
        return

    print("2. Testing Add History...")
    pm.add_history(test_cccd, "Diagnosis Test", "Treatment Test")
    
    data = pm.load_patient(test_cccd)
    last_record = data['history'][-1]
    
    if last_record['diagnosis'] == "Diagnosis Test":
        print("PASS: History Content")
    else:
        print("FAIL: History Content")

    if last_record['location'] == "Thành phố Đà Nẵng, Việt Nam":
        print("PASS: History Location Default")
    else:
        print(f"FAIL: History Location. Expected 'Thành phố Đà Nẵng, Việt Nam', got '{last_record['location']}'")

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)
    print("Test Complete.")

if __name__ == "__main__":
    test_patient_manager()
