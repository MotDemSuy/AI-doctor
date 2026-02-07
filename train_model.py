import os
import shutil
import random
from ultralytics import YOLO

def prepare_data(source_dirs, output_dir, split_ratio=0.8):
    """
    Tự động chia dữ liệu thành Train/Val để YOLO có thể học.
    Hỗ trợ gộp dữ liệu từ nhiều nguồn (MRI list, XRay list).
    """
    print(f"🔄 Đang chuẩn bị dữ liệu từ: {source_dirs}")
    
    # Xóa thư mục cũ nếu có để làm lại cho sạch
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Tạo folder train/val
    for split in ['train', 'val']:
        os.makedirs(os.path.join(output_dir, split), exist_ok=True)

    total_classes = 0
    
    for source_dir in source_dirs:
        if not os.path.exists(source_dir):
             print(f"⚠️ Bỏ qua nguồn không tồn tại: {source_dir}")
             continue
             
        # Duyệt qua từng loại bệnh trong nguồn này
        classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
        
        for class_name in classes:
            class_source = os.path.join(source_dir, class_name)
            images = [f for f in os.listdir(class_source) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if not images: continue
            
            total_classes += 1
            # Shuffle
            random.shuffle(images)
            split_idx = int(len(images) * split_ratio)
            
            train_imgs = images[:split_idx]
            val_imgs = images[split_idx:]
            
            # Copy training
            for img in train_imgs:
                src = os.path.join(class_source, img)
                dst_dir = os.path.join(output_dir, 'train', class_name)
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy(src, os.path.join(dst_dir, img))
            
            # Copy validation
            for img in val_imgs:
                src = os.path.join(class_source, img)
                dst_dir = os.path.join(output_dir, 'val', class_name)
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy(src, os.path.join(dst_dir, img))
            
    print(f"🎉 Đã chia dữ liệu xong! (Tổng {total_classes} loại bệnh). Sẵn sàng Training.\n")
    return total_classes > 0

def train_medical_model():
    print("🚀 BẮT ĐẦU QUÁ TRÌNH HUẤN LUYỆN AI Y TẾ...")
    
    # 1. Định nghĩa đường dẫn (Hỗ trợ cả MRI và XRay)
    raw_data_paths = [
        'Data/Datasets/MRI', 
        'Data/Datasets/XRay'
    ]
    ready_data_path = 'Data/Datasets/Medical_Ready' 
    
    # 2. Chuẩn bị dữ liệu
    if not prepare_data(raw_data_paths, ready_data_path):
        return

    # 3. Load Model
    model = YOLO('yolov8n-cls.pt') 

    # 4. Train Model
    results = model.train(
        data=ready_data_path, 
        epochs=10,        
        imgsz=224,       
        batch=4,          
        project='Medical_Training',
        name='My_Medical_AI'
    )
    
    print("\n✅ HUẤN LUYỆN HOÀN TẤT!")
    print(f"👉 Model của bạn được lưu tại: {os.path.abspath(results.save_dir)}\\weights\\best.pt")
    print("Hãy copy đường dẫn trên và cập nhật vào file cấu hình nếu muốn sử dụng.")

if __name__ == '__main__':
    train_medical_model()
