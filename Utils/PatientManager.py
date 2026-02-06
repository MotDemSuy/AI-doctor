import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'Patients')

class PatientManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

    def _get_file_path(self, cccd):
        return os.path.join(DATA_DIR, f"{cccd}.json")

    def load_patient(self, cccd):
        """Loads patient data by CCCD. Returns None if not found."""
        file_path = self._get_file_path(cccd)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_patient(self, cccd, info):
        """Creates or updates patient profile info."""
        file_path = self._get_file_path(cccd)
        
        # Load existing data to preserve history if updating info
        existing_data = self.load_patient(cccd)
        if existing_data:
            data = existing_data
            data['info'] = info # Update info
        else:
            data = {
                "cccd": cccd,
                "info": info,
                "history": []
            }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return data

    def add_history(self, cccd, diagnosis_content, treatment_suggestion=""):
        """Adds a medical record to the patient's history."""
        data = self.load_patient(cccd)
        if not data:
            return False

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": "Thành phố Đà Nẵng, Việt Nam",
            "diagnosis": diagnosis_content,
            "treatment_notes": treatment_suggestion
        }

        data['history'].append(record)

        file_path = self._get_file_path(cccd)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return True
