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

    def save_patient(self, cccd, info, genetic_data="", lifestyle="", habits="", medical_history=""):
        """Creates or updates patient profile info."""
        file_path = self._get_file_path(cccd)
        
        # Load existing data to preserve history if updating info
        existing_data = self.load_patient(cccd)
        if existing_data:
            data = existing_data
            data['info'] = info # Update info
            # Update specific fields if they are provided (not empty strings), otherwise keep existing
            # If they are not in existing data, default to empty string
            if genetic_data: data['genetic_data'] = genetic_data
            elif 'genetic_data' not in data: data['genetic_data'] = ""
            
            if lifestyle: data['lifestyle'] = lifestyle
            elif 'lifestyle' not in data: data['lifestyle'] = ""
            
            if habits: data['habits'] = habits
            elif 'habits' not in data: data['habits'] = ""
            
            if medical_history: data['medical_history'] = medical_history
            elif 'medical_history' not in data: data['medical_history'] = ""
            
        else:
            data = {
                "cccd": cccd,
                "info": info,
                "genetic_data": genetic_data,
                "lifestyle": lifestyle,
                "habits": habits,
                "medical_history": medical_history,
                "history": []
            }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return data

    def add_history(self, cccd, diagnosis_content, treatment_suggestion="", image_path=None):
        """Adds a medical record to the patient's history."""
        data = self.load_patient(cccd)
        if not data:
            return False

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": "Thành phố Đà Nẵng, Việt Nam",
            "diagnosis": diagnosis_content,
            "treatment_notes": treatment_suggestion,
            "image_path": image_path
        }

        data['history'].append(record)

        file_path = self._get_file_path(cccd)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return True
