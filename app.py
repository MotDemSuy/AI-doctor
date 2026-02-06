import streamlit as st
import os, time
from datetime import datetime
from dotenv import load_dotenv
from Utils.Agents import *
from Utils.PatientManager import PatientManager

# Page Config
st.set_page_config(page_title="Hệ Thống Chẩn Đoán Y Khoa AI", page_icon="🏥", layout="wide")

# Load Environment Variables
load_dotenv(dotenv_path='apikey.env')

# Initialize Manager
patient_manager = PatientManager()

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #007bff; color: white; font-weight: bold; }
    .report-box { background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #007bff; }
    .history-card { background-color: #ffffff; color: #333333; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .history-card h4 { color: #007bff; margin-top: 0; }
    .history-card p { color: #333333; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None
if "diagnosis_complete" not in st.session_state:
    st.session_state.diagnosis_complete = False
if "final_diagnosis" not in st.session_state:
    st.session_state.final_diagnosis = ""
if "full_report_context" not in st.session_state:
    st.session_state.full_report_context = ""
if "specialist_responses" not in st.session_state:
    st.session_state.specialist_responses = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "found_patient_info" not in st.session_state:
    st.session_state.found_patient_info = None
if "search_cccd" not in st.session_state:
    st.session_state.search_cccd = ""

# --- LOGIN SCREEN ---
if not st.session_state.current_patient:
    st.title("🏥 Hệ Thống Quản Lý Bệnh Nhân AI")
    
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        st.subheader("1. Tra Cứu Hồ Sơ")
        cccd_input = st.text_input("Nhập số CCCD:", max_chars=12, placeholder="Ví dụ: 0123456789")
        
        if st.button("🔍 Tra Cứu", type="primary"):
            if cccd_input:
                st.session_state.search_cccd = cccd_input
                patient_data = patient_manager.load_patient(cccd_input)
                
                if patient_data:
                    st.session_state.found_patient_info = patient_data['info']
                    st.success("✅ Đã tìm thấy hồ sơ! Vui lòng kiểm tra và cập nhật thông tin bên phải.")
                else:
                    st.session_state.found_patient_info = {} # Empty dict signals New User
                    st.info("ℹ️ Hồ sơ mới. Vui lòng nhập thông tin đăng ký bên phải.")
            else:
                st.error("Vui lòng nhập số CCCD.")

    with col2:
        st.subheader("2. Kiểm Tra & Đăng Nhập")
        
        # Determine values to pre-fill
        target_cccd = st.session_state.search_cccd
        defaults = st.session_state.found_patient_info if st.session_state.found_patient_info is not None else {}
        
        # Only show form if searched
        if target_cccd:
            with st.form("login_form"):
                st.write(f"Đang thao tác với CCCD: **{target_cccd}**")
                
                c_f1, c_f2 = st.columns(2)
                with c_f1:
                    f_name = st.text_input("Họ và Tên", value=defaults.get('name', ''))
                    f_gender_opts = ["Nam", "Nữ", "Khác"]
                    f_gender_idx = f_gender_opts.index(defaults.get('gender', 'Nam')) if defaults.get('gender') in f_gender_opts else 0
                    f_gender = st.selectbox("Giới tính", f_gender_opts, index=f_gender_idx)
                    
                    # DOB Handling
                    default_dob = datetime(1995, 1, 1).date()
                    if defaults.get('dob'):
                        try:
                            default_dob = datetime.strptime(defaults.get('dob'), "%Y-%m-%d").date()
                        except:
                            pass
                    f_dob = st.date_input(
                        "Ngày sinh",
                        value=default_dob,
                        min_value=datetime(1900, 1, 1).date(),
                        max_value=datetime.now().date(),
                        format="DD/MM/YYYY",
                        help="Nhập ngày/tháng/năm (Ví dụ: 20/05/1990)"
                    )

                with c_f2:
                    f_height = st.number_input("Chiều cao (cm)", min_value=0, max_value=250, value=int(defaults.get('height', 170)))
                    f_weight = st.number_input("Cân nặng (kg)", min_value=0, max_value=200, value=int(defaults.get('weight', 65)))
                
                submit_label = "💾 Lưu & Đăng Nhập"
                
                if st.form_submit_button(submit_label, type="primary"):
                    if f_name:
                        # Calculate Age
                        today = datetime.now().date()
                        age = today.year - f_dob.year - ((today.month, today.day) < (f_dob.month, f_dob.day))
                        
                        info = {
                            "name": f_name,
                            "dob": f_dob.strftime("%Y-%m-%d"),
                            "age": age, # Keep age for AI context compatibility
                            "gender": f_gender,
                            "height": f_height,
                            "weight": f_weight
                        }
                        # Save (Update or Create)
                        new_patient = patient_manager.save_patient(target_cccd, info)
                        st.session_state.current_patient = new_patient
                        st.success("Đã cập nhật thông tin!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Vui lòng nhập Họ tên.")
        else:
            st.info("👈 Vui lòng nhập CCCD và bấm 'Tra Cứu' ở cột bên trái trước.")

else:
    # --- LOGGED IN INTERFACE ---
    patient = st.session_state.current_patient
    info = patient['info']
    
    # Sidebar
    with st.sidebar:
        if st.button("⬅️ Đăng Xuất"):
            st.session_state.current_patient = None
            st.session_state.diagnosis_complete = False
            st.session_state.chat_history = []
            st.session_state.search_cccd = ""
            st.session_state.found_patient_info = None
            st.rerun()
            
        st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
        st.title(f"Hồ Sơ: {info['name']}")
        st.write(f"**CCCD:** {patient['cccd']}")
        st.write(f"**Ngày sinh:** {info.get('dob', 'N/A')}")
        st.write(f"**Tuổi:** {info['age']}")
        st.write(f"**Giới tính:** {info['gender']}")
        
        # Calculate BMI
        bmi = info['weight'] / ((info['height']/100) ** 2)
        st.write(f"**BMI:** {bmi:.1f}")
        
        # BMI Analysis Feature
        st.markdown("---")
        st.write("### 📊 Phân Tích Thể Trạng")
        if st.button("🔍 Phân Tích & Lời Khuyên"):
            with st.spinner("AI đang tính toán..."):
                try:
                    # Prepare data for AI
                    bmi_report_context = f"""
                    Họ tên: {info['name']}
                    Tuổi: {info['age']}
                    Giới tính: {info['gender']}
                    Chiều cao: {info['height']} cm
                    Cân nặng: {info['weight']} kg
                    BMI: {bmi:.1f}
                    """
                    advisor = BMIAdvisor(bmi_report_context)
                    advice = advisor.run()
                    st.success("Kết quả phân tích:")
                    st.markdown(advice)
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
        
        st.markdown("---")
        st.write("### 📜 Lịch Sử Khám")
        for record in reversed(patient['history']):
             with st.expander(f"{record['timestamp']}"):
                 st.write(f"**Nơi khám:** {record['location']}")
                 st.caption(record['diagnosis'][:100] + "...")

    # Main Content
    st.title("🏥 Chẩn Đoán Y Khoa AI")
    
    # Tabs for Diagnosis vs History Details
    tab1, tab2 = st.tabs(["🩺 Khám Bệnh Mới", "📂 Chi Tiết Lịch Sử"])
    
    with tab1:
        st.markdown(f"### Xin chào, {info['name']}. Hôm nay bạn cảm thấy thế nào?")
        
        # Input Form
        with st.form("medical_form"):
            symptoms = st.text_area(
                "Mô tả triệu chứng, các vấn đề sức khỏe...",
                height=150,
                placeholder="Ví dụ: Đau đầu, chóng mặt, buồn nôn..."
            )
            submitted = st.form_submit_button("Bắt Đầu Chẩn Đoán")

        # Mapping string names to Class objects
        AGENT_MAP = {
            "Emergency": Emergency,
            "Cardiologist": Cardiologist,
            "Pulmonologist": Pulmonologist,
            "Gastroenterologist": Gastroenterologist,
            "Neurologist": Neurologist,
            "Endocrinologist": Endocrinologist,
            "Surgeon": Surgeon,
            "OBGYN": OBGYN,
            "Pediatrician": Pediatrician,
            "ENT": ENT,
            "Dermatologist": Dermatologist,
            "Ophthalmologist": Ophthalmologist,
            "Dentist": Dentist,
            "Psychiatrist": Psychiatrist
        }
        
        VN_NAMES = {
            "Emergency": "Cấp Cứu",
            "Cardiologist": "Tim Mạch",
            "Pulmonologist": "Hô Hấp",
            "Gastroenterologist": "Tiêu Hóa",
            "Neurologist": "Thần Kinh",
            "Endocrinologist": "Nội Tiết",
            "Surgeon": "Ngoại Khoa",
            "OBGYN": "Sản Phụ Khoa",
            "Pediatrician": "Nhi Khoa",
            "ENT": "Tai Mũi Họng",
            "Dermatologist": "Da Liễu",
            "Ophthalmologist": "Nhãn Khoa",
            "Dentist": "Răng Hàm Mặt",
            "Psychiatrist": "Tâm Lý"
        }

        if submitted and symptoms:
            # Reset chat if new diagnosis started
            st.session_state.chat_history = []
            
            full_report = f"""
            Họ tên: {info['name']}
            Tuổi: {info['age']}
            Giới tính: {info['gender']}
            Chiều cao: {info['height']} cm
            Cân nặng: {info['weight']} kg
            BMI: {bmi:.1f}
            
            Triệu chứng/Tiền sử:
            {symptoms}
            """
            st.session_state.full_report_context = full_report
            
            st.markdown("---")
            st.subheader("1. Phân Loại & Điều Phối (Bác sĩ Đa khoa)")
            
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            try:
                # Step 1: Generalist Triage
                status_text.text("👨‍⚕️ Bác sĩ Đa khoa đang đánh giá sơ bộ...")
                generalist = Generalist(full_report)
                triage_result = generalist.run()
                
                # Parse specialists
                needed_specialists = []
                for key in AGENT_MAP.keys():
                    if key in triage_result:
                        needed_specialists.append(key)
                
                if not needed_specialists:
                    st.warning("Không chuyên khoa cụ thể nào được đề xuất rõ ràng. Sẽ tham vấn Nội Tổng Quát.")
                    needed_specialists = ["Cardiologist", "Gastroenterologist", "Pulmonologist"]
                    
                st.success(f"📌 Đã chỉ định: {', '.join([VN_NAMES.get(s, s) for s in needed_specialists])}")
                progress_bar.progress(0.2)
                
                # Step 2: Run Specialists
                st.subheader("2. Tham Vấn Chuyên Khoa")
                responses = {}
                
                cols = st.columns(len(needed_specialists)) if len(needed_specialists) <= 3 else st.columns(3)
                step_increment = 0.6 / len(needed_specialists)
                current_progress = 0.2
                
                for i, specialist_name in enumerate(needed_specialists):
                    status_text.text(f"Đang tham vấn {VN_NAMES.get(specialist_name, specialist_name)}... (Vui lòng chờ AI)")
                    
                    agent_class = AGENT_MAP[specialist_name]
                    agent = agent_class(full_report)
                    response = agent.run()
                    responses[specialist_name] = response
                    
                    col_idx = i % 3
                    with cols[col_idx] if len(needed_specialists) > 3 else cols[i]:
                        with st.expander(f"📋 {VN_NAMES.get(specialist_name, specialist_name)}", expanded=True):
                            st.markdown(response)
                    
                    current_progress += step_increment
                    progress_bar.progress(min(current_progress, 0.8))
                    
                    if i < len(needed_specialists) - 1:
                        status_text.text("Đang nghỉ một chút để tránh quá tải server...")
                        time.sleep(2) # Reduced sleep time for better UX
                
                st.session_state.specialist_responses = responses

                # Step 3: Multidisciplinary Team
                st.subheader("3. Kết Luận Hội Đồng Chẩn Đoán")
                status_text.text("👨‍⚕️ Hội đồng Y khoa đang tổng hợp kết quả...")
                
                combined_reports = ""
                for name, content in responses.items():
                    combined_reports += f"\\n--- Báo cáo từ {VN_NAMES.get(name, name)} ---\\n{content}\\n"
                    
                team_agent = MultidisciplinaryTeam(combined_reports)
                final_diagnosis = team_agent.run()
                
                # --- SAVE TO HISTORY ---
                patient_manager.add_history(
                    cccd=patient['cccd'],
                    diagnosis_content=final_diagnosis,
                    treatment_suggestion="Xem chi tiết trong báo cáo."
                )
                # Refresh session data to show new history immediatey
                st.session_state.current_patient = patient_manager.load_patient(patient['cccd'])
                
                st.session_state.final_diagnosis = final_diagnosis
                st.session_state.diagnosis_complete = True
                
                progress_bar.progress(1.0)
                status_text.success("Hoàn tất chẩn đoán & Đã lưu vào hồ sơ!")
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {str(e)}")

        # --- DISPLAY RESULTS FROM STATE ---
        if st.session_state.diagnosis_complete:
            st.info(st.session_state.final_diagnosis)
            
            st.download_button(
                label="Tải Về Hồ Sơ Bệnh Án",
                data=st.session_state.final_diagnosis,
                file_name=f"HoSo_{info['name'].replace(' ', '_')}.txt",
                mime="text/plain"
            )

            # --- CHAT INTERFACE ---
            st.markdown("---")
            st.subheader("💬 Tư Vấn Chuyên Sâu Sau Chẩn Đoán")
            
            col_chat_1, col_chat_2 = st.columns([1, 3])
            
            with col_chat_1:
                st.markdown("**Chọn Chuyên Gia:**")
                consultant_type = st.radio(
                    "Chọn người tư vấn:",
                    ["Nutritionist", "LifestyleAdvisor"],
                    format_func=lambda x: "🍎 Dinh Dưỡng" if x == "Nutritionist" else "🧘 Lối Sống"
                )
            
            with col_chat_2:
                st.markdown(f"**Trò chuyện với {('Chuyên gia Dinh Dưỡng' if consultant_type == 'Nutritionist' else 'Chuyên gia Lối Sống')}**")
                
                # Display Chat History
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # Chat Input
                if prompt := st.chat_input("Đặt câu hỏi cho bác sĩ..."):
                    # Add user message
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Generate response
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        message_placeholder.markdown("AI đang soạn tin nhắn...")
                        
                        try:
                            # Prepare context
                            diagnosis_context = f"""
                            BÁO CÁO CỦA BỆNH NHÂN:
                            {st.session_state.full_report_context}
                            
                            KẾT LUẬN CHẨN ĐOÁN:
                            {st.session_state.final_diagnosis}
                            """
                            
                            # Convert chat history to string
                            history_text = "\\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history[-5:]])
                            
                            # Run Consultant Agent
                            consultant = Consultant(
                                diagnosis_context=diagnosis_context,
                                consultant_type=consultant_type,
                                chat_history=history_text,
                                user_question=prompt
                            )
                            full_response = consultant.run()
                            message_placeholder.markdown(full_response)
                            
                            # Add assistant message
                            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                            
                        except Exception as e:
                            message_placeholder.error(f"Lỗi: {e}")

    with tab2:
        st.subheader(f"📂 Hồ Sơ Bệnh Án Của {info['name']}")
        if not patient['history']:
            st.info("Chưa có lịch sử khám bệnh.")
        else:
            for i, record in enumerate(reversed(patient['history'])):
                st.markdown(f"""
                <div class="history-card">
                    <h4>📅 {record['timestamp']}</h4>
                    <p><b>📍 Tại:</b> {record['location']}</p>
                    <hr>
                    <p><b>🩺 Chẩn đoán:</b></p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
                        {record['diagnosis']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
