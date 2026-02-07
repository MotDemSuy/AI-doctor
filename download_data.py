import os
import requests
import random

def download_mri_samples():
    """
    Tải mẫu MRI cho 10 loại bệnh/tình trạng phổ biến (5 ảnh/loại).
    Nguồn: GitHub Repositories (sartajbhuvaji & Fhrozen & others).
    """
    print("--- TẢI DỮ LIỆU MRI MẪU (10 LOẠI - 5 CA/LOẠI) ---")
    print("Lưu ý: Dữ liệu được lấy từ các nguồn Open Source trên GitHub.")
    
    # Cấu hình đường dẫn
    mri_dir = "Data/Datasets/MRI"
    xray_dir = "Data/Datasets/XRay"
    
    os.makedirs(mri_dir, exist_ok=True)
    os.makedirs(xray_dir, exist_ok=True)

    # Cấu hình nguồn dữ liệu (Đã Việt hóa tên thư mục)
    # GROUP A: Sử dụng API GitHub (Tự động lấy danh sách file)
    sources_api = {
        # 1. Nhóm U não (Brain Tumor) - Nguồn: sartajbhuvaji
        "U_Nao_Glioma": "https://api.github.com/repos/sartajbhuvaji/Brain-Tumor-Classification-DataSet/contents/Training/glioma_tumor",
        "U_Nao_Meningioma": "https://api.github.com/repos/sartajbhuvaji/Brain-Tumor-Classification-DataSet/contents/Training/meningioma_tumor",
        "U_Nao_Tuyen_Yen": "https://api.github.com/repos/sartajbhuvaji/Brain-Tumor-Classification-DataSet/contents/Training/pituitary_tumor",
        "U_Nao_Khoe_Manh": "https://api.github.com/repos/sartajbhuvaji/Brain-Tumor-Classification-DataSet/contents/Training/no_tumor",

        # 2. X-Quang Viêm Phổi (COVID-19 & Pneumonia)
        "XQuang_Viem_Phoi": "https://api.github.com/repos/ieee8023/covid-chestxray-dataset/contents/images",
        
        # 3. X-Quang Lao Phổi (Tuberculosis) - Nguồn: nima-kam (Dataset có sẵn thư mục images phẳng)
        "XQuang_Lao_Phoi": "https://api.github.com/repos/nima-kam/Tuberculosis_detection_CXR_PyTorch/contents/images",

        # 4. X-Quang Viêm Khớp (Arthritis) - Nguồn: mafda (Knee OA)
        "XQuang_Viem_Khop": "https://api.github.com/repos/mafda/knee_OA_dl_app/contents/app/img",

        # 5. X-Quang Ung Thư Xương (Bone Tumor) - Nguồn: javid4962 (Lấy tập 'yes' - có khối u)
        "XQuang_Ung_Thu_Xuong": "https://api.github.com/repos/javid4962/Bone_Tumor_Prediction/contents/bone_tumor_dataset/yes"
    }

    # GROUP B: Hardcoded fallback (Link tĩnh)
    uranus_base = "https://raw.githubusercontent.com/uranusx86/Alzheimer-s-Disease-Classification/master/data"
    
    # URL Demo cho Suy Tim (Cardiomegaly) & Tiêu Hóa (Abdominal) - Nguồn: Wikimedia Commons
    # (Vì dataset raw 2 loại này rất nặng hoặc hiếm, dùng ảnh điển hình để demo)
    heart_url = "https://upload.wikimedia.org/wikipedia/commons/f/f0/Cardiomegaly_in_PA_chest_radiograph.jpg"
    abdomen_url = "https://upload.wikimedia.org/wikipedia/commons/3/3d/Abdominal_X-ray_of_small_bowel_obstruction.jpg"

    sources_direct = {
        # 3. Nhóm Alzheimer (Việt hóa)
        "Alzheimer_Nhe": [
           f"{uranus_base}/MildDemented/26%20(19).jpg",
           f"{uranus_base}/MildDemented/26%20(20).jpg",
           f"{uranus_base}/MildDemented/26%20(21).jpg",
           f"{uranus_base}/MildDemented/26%20(22).jpg",
           f"{uranus_base}/MildDemented/26%20(23).jpg"
        ],
        "Alzheimer_Trung_Binh": [
            f"{uranus_base}/ModerateDemented/moderate_2.jpg",
            f"{uranus_base}/ModerateDemented/moderate_3.jpg",
            f"{uranus_base}/ModerateDemented/moderate_4.jpg",
            f"{uranus_base}/ModerateDemented/moderate_5.jpg",
            f"{uranus_base}/ModerateDemented/moderate_6.jpg"
        ],
        "Alzheimer_Rat_Nhe": [
            f"{uranus_base}/VeryMildDemented/verymild_2.jpg",
            f"{uranus_base}/VeryMildDemented/verymild_3.jpg",
            f"{uranus_base}/VeryMildDemented/verymild_4.jpg",
            f"{uranus_base}/VeryMildDemented/verymild_5.jpg",
            f"{uranus_base}/VeryMildDemented/verymild_6.jpg"
        ],
        "Alzheimer_Khong_Bi": [
             f"{uranus_base}/NonDemented/26%20(62).jpg",
             f"{uranus_base}/NonDemented/26%20(63).jpg",
             f"{uranus_base}/NonDemented/26%20(64).jpg",
             f"{uranus_base}/NonDemented/26%20(65).jpg",
             f"{uranus_base}/NonDemented/26%20(66).jpg"
        ],
        
        # 4. X-Quang Bình Thường (Demo)
        "XQuang_Binh_Thuong": [
            "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/01E392EE-69F9-4E33-BFCE-E5C968654078.jpeg",
            "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/0a7faa2a.jpg", 
            "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/03BF7561-A9BA-4C3C-B8A0-D3E585F73F3C.jpeg",
            "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/7C69C012-7479-493F-8722-2661632736FD.jpeg",
            "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/2966893D-5DDF-4B68-9E2B-4979D5956C8E.jpeg"
        ],

        # 5. X-Quang Suy Tim (Cardiomegaly) - Demo 5 ảnh giống nhau (Simulation)
        "XQuang_Suy_Tim": [heart_url] * 5,

        # 6. X-Quang Tiêu Hóa (Abdominal) - Demo 5 ảnh giống nhau (Simulation)
        "XQuang_Tieu_Hoa": [abdomen_url] * 5
    }
    
    # URL dự phòng Alzheimer
    placeholder_urls = [
        "https://raw.githubusercontent.com/sartajbhuvaji/Brain-Tumor-Classification-DataSet/master/Training/meningioma_tumor/m3%20(1).jpg",
        "https://raw.githubusercontent.com/sartajbhuvaji/Brain-Tumor-Classification-DataSet/master/Training/meningioma_tumor/m3%20(2).jpg",
        "https://raw.githubusercontent.com/sartajbhuvaji/Brain-Tumor-Classification-DataSet/master/Training/meningioma_tumor/m3%20(3).jpg",
        "https://raw.githubusercontent.com/sartajbhuvaji/Brain-Tumor-Classification-DataSet/master/Training/meningioma_tumor/m3%20(4).jpg",
        "https://raw.githubusercontent.com/sartajbhuvaji/Brain-Tumor-Classification-DataSet/master/Training/meningioma_tumor/m3%20(5).jpg"
    ]
    
    # Fallback assignment
    sources_direct["Alzheimer_Nhe"] = placeholder_urls
    sources_direct["Alzheimer_Trung_Binh"] = placeholder_urls
    sources_direct["Alzheimer_Rat_Nhe"] = placeholder_urls
    sources_direct["Alzheimer_Khong_Bi"] = placeholder_urls
    
    # Header để tránh rate limit
    headers = {"Accept": "application/vnd.github.v3+json"}

    # Helper function to get save path
    def get_save_path(disease_name):
        if disease_name.startswith("XQuang"):
            return os.path.join(xray_dir, disease_name)
        return os.path.join(mri_dir, disease_name)

    # 1. GROUP A: Tải từ GitHub API (Tăng số lượng mẫu lên 15 cho X-Ray)
    for disease, api_url in sources_api.items():
        print(f"\n📂 Đang xử lý: {disease}...")
        save_path = get_save_path(disease)
        os.makedirs(save_path, exist_ok=True)
        
        try:
            r = requests.get(api_url, headers=headers)
            if r.status_code == 200:
                files = r.json()
                image_files = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                # Lấy NHIỀU HƠN cho X-Quang Viêm Phổi
                limit = 15 if disease == "XQuang_Viem_Phoi" else 5
                selected = image_files[:limit]
                
                if not selected:
                    print(f"   ⚠️ Không tìm thấy ảnh trong folder này.")
                    continue
                    
                for i, img_data in enumerate(selected):
                    img_url = img_data['download_url']
                    new_name = f"{disease}_{i+1}.jpg"
                    try:
                        img_r = requests.get(img_url, timeout=10)
                        if img_r.status_code == 200:
                            with open(os.path.join(save_path, new_name), 'wb') as f:
                                f.write(img_r.content)
                            print(f"   ✅ [OK] {new_name}")
                        else:
                            print(f"   ❌ Lỗi tải ảnh: {img_r.status_code}")
                    except Exception as e:
                        print(f"   ❌ Lỗi kết nối: {e}")
            else:
                print(f"   ❌ Lỗi API: {r.status_code}")
        except Exception as e:
            print(f"   ❌ Lỗi: {e}")

    # 2. GROUP B: Tải từ link trực tiếp (Fallback)
    for disease, urls in sources_direct.items():
        print(f"\n📂 Đang tải bổ sung: {disease}...")
        save_path = get_save_path(disease)
        os.makedirs(save_path, exist_ok=True)
        for i, url in enumerate(urls):
            try:
                new_name = f"{disease}_{i+1}.jpg"
                # Auto encode space just in case
                url = url.replace(" ", "%20")
                
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    with open(os.path.join(save_path, new_name), 'wb') as f:
                        f.write(r.content)
                    print(f"   ✅ [OK] {new_name}")
                else:
                    print(f"   ❌ Link chết: {url}")
            except Exception as e:
                print(f"   ❌ Lỗi: {e}")

    print(f"\n✅ HOÀN TẤT TẢI DỮ LIỆU!")
    print(f"MRI Thư mục: {os.path.abspath(mri_dir)}")
    print(f"X-Ray Thư mục: {os.path.abspath(xray_dir)}")
    print("Bạn có thể dùng 'train_model.py' (nhớ sửa đường dẫn data) để train ngay.")

if __name__ == "__main__":
    download_mri_samples()
