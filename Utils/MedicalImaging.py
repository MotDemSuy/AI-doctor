try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None

import os
import cv2
import numpy as np
from PIL import Image

class MedicalImageAnalyzer:
    def __init__(self, model_path=None):
        """
        Khởi tạo bộ phân tích hình ảnh.
        :param model_path: Đường dẫn đến file model (.pt). Nếu None, dùng model classify mặc định (yolov8n-cls.pt).
        """
        if YOLO is None:
            self.model = None
            print("Ultralytics not installed. Please install it to use this feature.")
            return

        self.default_model = "yolov8n-cls.pt"
        self.model_path = model_path if model_path and os.path.exists(model_path) else self.default_model
        
        try:
            self.model = YOLO(self.model_path)
            print(f"Loaded YOLO model: {self.model_path}")
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None

    def analyze(self, image_source):
        """
        Phân tích hình ảnh.
        :param image_source: Đường dẫn ảnh hoặc numpy array.
        :return: Dict kết quả (class, confidence, annotated_image_path nếu có).
        """
        if not self.model:
            return {"error": "Model not loaded properly."}

        try:
            # Predict
            results = self.model(image_source)
            
            # Process result
            result = results[0]
            
            top5_conf = []
            top5_class = []
            
            if hasattr(result, 'probs') and result.probs is not None:
                # Classification task
                probs = result.probs
                # Top 1 class
                top1_idx = probs.top1
                top1_conf = probs.top1conf.item()
                top1_name = result.names[top1_idx]
                
                return {
                    "type": "classification",
                    "top_match": top1_name,
                    "confidence": top1_conf,
                    "summary": f"Phát hiện: {top1_name} ({top1_conf:.2%})"
                }
                
            elif hasattr(result, 'boxes') and result.boxes is not None:
                # Detection task
                detections = []
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = result.names[cls_id]
                    detections.append(f"{label} ({conf:.2%})")
                
                return {
                    "type": "detection",
                    "detections": detections,
                    "summary": f"Các vùng phát hiện: {', '.join(detections)}" if detections else "Không phát hiện bất thường rõ rệt."
                }
            
            return {"summary": "Không xác định được kết quả từ model."}
            
        except Exception as e:
            return {"error": f"Lỗi phân tích: {str(e)}"}
