from Utils.PatientManager import PatientManager
from Utils.PatientManager import PatientManager
from Utils.Agents import TreatmentPlanner, PharmacogenomicsAdvisor, DiagnosticExplainer
import os

def test_manager():
    print("Testing PatientManager...")
    pm = PatientManager()
    cccd = "TEST_001"
    info = {"name": "Test Patient", "age": 30}
    
    # Save with new fields
    pm.save_patient(cccd, info, 
                    genetic_data="Gen A mutation", 
                    lifestyle="Active", 
                    habits="None", 
                    medical_history="None")
    
    # Load
    data = pm.load_patient(cccd)
    if data['genetic_data'] == "Gen A mutation" and data['lifestyle'] == "Active":
        print("PatientManager Test PASSED!")
    else:
        print("PatientManager Test FAILED!")
        print(data)

def test_agents():
    print("Testing Agents instantiation...")
    report = "Patient: Test. Condition: Flu. Genetics: Gen A mutation."
    
    try:
        planner = TreatmentPlanner(report)
        assert planner.role == "TreatmentPlanner"
        
        advisor = PharmacogenomicsAdvisor(report)
        assert advisor.role == "PharmacogenomicsAdvisor"
        
        explainer = DiagnosticExplainer(report)
        assert explainer.role == "DiagnosticExplainer"
        print("Agents instantiation PASSED!")
    except Exception as e:
        print(f"Agents instantiation FAILED: {e}")

if __name__ == "__main__":
    test_manager()
    test_agents()
