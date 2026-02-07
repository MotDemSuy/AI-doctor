from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
import time

class Agent:
    def __init__(self, medical_report=None, role=None, extra_info=None):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info
        # Initialize the prompt based on role and other info
        self.prompt_template = self.create_prompt_template()
        
        # Breakdown: Meditron-7b was echoing prompts. 
        # Switching everything to llama3 for consistent instruction following.
        selected_model = "llama3:8b"
            
        # Initialize the model - Local Ollama
        self.model = ChatOllama(model=selected_model, temperature=0)

    def create_prompt_template(self):
        if self.role == "Generalist":
            # Bác sĩ Đa khoa - Triage Agent
            template = """
            Bạn là một Bác sĩ Đa khoa giàu kinh nghiệm làm việc tại phòng khám sàng lọc.
            Nhiệm vụ: Phân tích triệu chứng của bệnh nhân và CHỈ ĐỊNH các chuyên khoa phù hợp nhất để khám chuyên sâu.
            
            Danh sách các chuyên khoa hiện có:
            - Emergency (Hồi sức cấp cứu - Cho các ca nguy kịch, ngất, khó thở cấp, tai nạn...)
            - Cardiologist (Tim mạch - Đau ngực, huyết áp, nhịp tim...)
            - Pulmonologist (Hô hấp - Ho, khó thở, phổi...)
            - Gastroenterologist (Tiêu hóa - Đau bụng, dạ dày, gan mật...)
            - Neurologist (Thần kinh - Đau đầu, chóng mặt, tê bì, đột quỵ...)
            - Endocrinologist (Nội tiết - Tiểu đường, tuyến giáp...)
            - Surgeon (Ngoại khoa - Chấn thương, khối u cần mổ, ngoại tổng quát...)
            - OBGYN (Sản Phụ khoa - Phụ nữ mang thai, bệnh phụ khoa...)
            - Pediatrician (Nhi khoa - Trẻ em dưới 16 tuổi)
            - ENT (Tai Mũi Họng)
            - Dermatologist (Da liễu - Bệnh ngoài da)
            - Ophthalmologist (Mắt)
            - Dentist (Răng Hàm Mặt)
            - Psychiatrist (Tâm lý - Căng thẳng, trầm cảm, lo âu...)

            Báo cáo của bệnh nhân: {medical_report}

            Yêu cầu trả về:
            Chỉ trả về một danh sách các tên chuyên khoa bằng tiếng Anh (để code xử lý) nằm trong danh sách trên, ngăn cách bởi dấu phẩy.
            Ví dụ: Cardiologist, Emergency
            Không giải thích gì thêm.
            """
        elif self.role == "MultidisciplinaryTeam":
            # Hội đồng chẩn đoán
            template = f"""
            Bạn là Hội đồng Chẩn đoán Y khoa đa chuyên khoa (Medical Board).
            Nhiệm vụ: Tổng hợp các báo cáo từ các bác sĩ chuyên khoa và đưa ra Chẩn đoán cuối cùng xác đáng nhất.
            
            Các báo cáo từ chuyên khoa:
            {self.extra_info.get('specialist_reports', '')}
            
            Hãy đưa ra kết luận theo định dạng sau (bằng Tiếng Việt):
            # KẾT LUẬN HỘI ĐỒNG
            1. **Chẩn đoán sơ bộ**: ...
            2. **Phân tích tổng hợp**: (Tóm tắt các phát hiện chính từ các chuyên khoa)
            3. **Cơ sở lập luận (Explainable AI)**: 
               - **Tại sao chọn chẩn đoán này?**: (Liệt kê các triệu chứng chính và kết quả cận lâm sàng ủng hộ).
               - **Tại sao loại trừ?**: (Lý do loại trừ các khả năng khác).
            4. **Đề xuất điều trị/Cận lâm sàng tiếp theo**: ...
            5. **Lời khuyên cho bệnh nhân**: ...
            """
        elif self.role == "DiagnosticExplainer":
            # Chuyên gia Giải thích Chẩn đoán (XAI)
            template = """
            Bạn là một Chuyên gia Giải thích Y khoa (Medical Explainability Expert).
            Nhiệm vụ: Giải thích chi tiết logic đằng sau chẩn đoán cho bác sĩ và bệnh nhân, đảm bảo tính minh bạch (Transparency).
            
            Dữ liệu đầu vào:
            {medical_report}
            
            Hãy trả lời bằng Tiếng Việt, tập trung vào tư duy phản biện:
            1. **Bản đồ Tư duy Chẩn đoán**: (Vẽ ra logic: Triệu chứng A + Yếu tố nguy cơ B => Khả năng cao là bệnh X).
            2. **Phân tích Pros/Cons**: 
               - **Yếu tố Ủng hộ chẩn đoán (Pros)**: ...
               - **Yếu tố Mâu thuẫn/Chưa rõ (Cons)**: ...
            3. **Độ tin cậy của chẩn đoán**: (Đánh giá mức độ chắc chắn: Cao/Trung bình/Thấp và lý do).
            4. **Các Giả thuyết Thay thế**: (Nếu không phải bệnh X, thì khả năng tiếp theo là gì?).
            """
        elif self.role == "Consultant":
            # Chuyên gia tư vấn (Chat mode)
            consultant_type = self.extra_info.get('consultant_type', 'General')
            diagnosis_context = self.extra_info.get('diagnosis_context', '')
            chat_history = self.extra_info.get('chat_history', '')
            
            if consultant_type == "Nutritionist":
                role_name = "Chuyên gia Dinh Dưỡng"
                focus = "chế độ ăn uống, thực phẩm nên ăn/kiêng, thực đơn mẫu"
            elif consultant_type == "LifestyleAdvisor":
                role_name = "Chuyên gia Lối Sống"
                focus = "chế độ tập luyện, giấc ngủ, kiểm soát căng thẳng, thói quen sinh hoạt"
            else:
                role_name = "Trợ lý Y tế"
                focus = "thông tin y tế chung"

            template = f"""
            Bạn là {role_name} chuyên nghiệp, tận tâm.
            
            Thông tin bệnh nhân & Chẩn đoán từ bác sĩ:
            {diagnosis_context}
            
            Lịch sử trò chuyện:
            {chat_history}
            
            Người dùng hỏi: {{medical_report}} (Ở đây là câu hỏi mới nhất của người dùng)
            
            Nhiệm vụ: Trả lời câu hỏi của người dùng, tập trung sâu vào {focus} để hỗ trợ quá trình điều trị.
            Lời khuyên phải cụ thể, thiết thực và dựa trên chẩn đoán y khoa đã có.
            Giọng văn: Thân thiện, khích lệ, chuyên nghiệp.
            """
        elif self.role == "BMIAdvisor":
            # Chuyên gia phân tích BMI & Cân nặng
            template = """
            Bạn là một Chuyên gia Dinh dưỡng và Thể hình (Certified Personal Trainer & Nutritionist).
            Nhiệm vụ: Phân tích chỉ số cơ thể và đưa ra lời khuyên tăng/giảm cân cụ thể.
            
            Thông tin bệnh nhân:
            {medical_report}
            
            Hãy trả lời ngắn gọn, súc tích bằng Tiếng Việt:
            1. **Đánh giá tình trạng**: (Gầy/Bình thường/Thừa cân/Béo phì? Mức độ nào?).
            2. **Mục tiêu**: Cần tăng/giảm bao nhiêu kg để về mức Chuẩn (BMI 18.5 - 24.9)?
            3. **Lời khuyên Dinh dưỡng**: (Nên ăn gì, kiêng gì? Ví dụ thực phẩm).
            4. **Lời khuyên Vận động**: (Bài tập phù hợp? Cường độ?).
            
            Giọng văn: Thân thiện, khích lệ.
            """
        elif self.role == "TreatmentPlanner":
            # Chuyên gia Lập Kế Hoạch Điều Trị Cá Nhân Hóa
            template = """
            Bạn là một Chuyên gia Lập Kế Hoạch Điều Trị Cá Nhân Hóa (Personalized Treatment Planner) hàng đầu.
            Nhiệm vụ: Xây dựng một phác đồ điều trị chi tiết, riêng biệt cho bệnh nhân dựa trên dữ liệu tổng hợp (Gen, Lối sống, Tiền sử...).
            
            Dữ liệu bệnh nhân và Chẩn đoán hiện tại:
            {medical_report}
            
            Hãy trả lời bằng Tiếng Việt một cách chuyên nghiệp và chi tiết:
            1. **Phân tích Yếu tố Cá nhân**: (Phân tích sâu xem Gen, Lối sống, và Thói quen cụ thể của bệnh nhân ảnh hưởng thế nào đến bệnh lý và quá trình điều trị).
            2. **Phác đồ Điều trị Cá nhân hóa Tối ưu**: (Đề xuất phương án điều trị cụ thể, bao gồm thuốc men và can thiệp y tế, được điều chỉnh riêng cho cơ địa này).
            3. **Kế hoạch Điều chỉnh Lối sống & Dinh dưỡng**: (Các thay đổi cụ thể về sinh hoạt cần thiết để hỗ trợ điều trị).
            4. **Lưu ý & Tiên lượng**: (Cảnh báo các rủi ro tiềm ẩn dựa trên gene/tiền sử và dự đoán kết quả điều trị).
            """
        elif self.role == "PharmacogenomicsAdvisor":
            # Chuyên gia Dược lý Di truyền & An toàn thuốc
            template = """
            Bạn là một Chuyên gia Dược lý Di truyền (Pharmacogenomics Specialist) và Dược lâm sàng.
            Nhiệm vụ: Phân tích dữ liệu gen, CƠ ĐỊA, DỊ ỨNG và đặc điểm sinh học để dự đoán phản ứng thuốc, tối ưu hóa việc dùng thuốc.
            
            Dữ liệu bệnh nhân:
            {medical_report}
            
            Hãy trả lời bằng Tiếng Việt:
            1. **Dự đoán Phản ứng Thuốc**: (Phân tích khả năng chuyển hóa thuốc dựa trên cơ địa/gen/lối sống. Nhóm thuốc nào hiệu quả cao? Nhóm nào cần thận trọng?).
            2. **Cảnh báo Tác dụng phụ & Dị ứng**: (Lưu ý đặc biệt về tiền sử dị ứng đã khai báo và các rủi ro tiềm ẩn).
            3. **Khuyến nghị Liều lượng & Cách dùng**: (Cần điều chỉnh liều lượng thế nào so với tiêu chuẩn? Cần theo dõi chỉ số gì?).
            4. **Đề xuất Thay thế (Nếu cần)**: (Gợi ý các loại thuốc hoặc phương pháp thay thế an toàn hơn nếu có nguy cơ cao).
            """
        else:
            # Các bác sĩ chuyên khoa
            # ... (Existing code) ...
            vn_role_map = {
                "Emergency": "Bác sĩ Hồi sức Cấp cứu",
                "Cardiologist": "Bác sĩ Tim mạch",
                "Pulmonologist": "Bác sĩ Hô hấp",
                "Gastroenterologist": "Bác sĩ Tiêu hóa - Gan mật",
                "Neurologist": "Bác sĩ Thần kinh",
                "Endocrinologist": "Bác sĩ Nội tiết",
                "Surgeon": "Bác sĩ Ngoại khoa",
                "OBGYN": "Bác sĩ Sản Phụ khoa",
                "Pediatrician": "Bác sĩ Nhi khoa",
                "ENT": "Bác sĩ Tai Mũi Họng",
                "Dermatologist": "Bác sĩ Da liễu",
                "Ophthalmologist": "Bác sĩ Mắt",
                "Dentist": "Bác sĩ Răng Hàm Mặt",
                "Psychiatrist": "Bác sĩ Tâm lý"
            }
            vn_role = vn_role_map.get(self.role, self.role)
            
            template = f"""
            Đóng vai: {vn_role}.
            Nhiệm vụ: Phân tích báo cáo y tế của bệnh nhân dưới góc độ chuyên môn của bạn.
            
            Báo cáo của bệnh nhân: {{medical_report}}
            
            Hãy trả lời bằng Tiếng Việt theo cấu trúc:
            **1. Đánh giá chuyên khoa**: (Nhận định các triệu chứng liên quan đến chuyên khoa của bạn. Nếu không có gì bất thường thuộc chuyên khoa, hãy nói rõ).
            **2. Chẩn đoán phân biệt**: (Các bệnh lý có thể xảy ra).
            **3. Đề xuất**: (Các xét nghiệm cận lâm sàng cần làm thêm hoặc hướng điều trị).
            
            Lưu ý: Chỉ tập trung vào chuyên môn của {vn_role}.
            """
        
        return PromptTemplate.from_template(template)
    
    def run(self):
        # print(f"{self.role} is running...")
        prompt = self.prompt_template.format(medical_report=self.medical_report)
        
        # Local Ollama - No Rate Limits needed!
        try:
            print(f"   [{self.role}] Processing with Ollama ({self.model.model})...")
            response = self.model.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error in {self.role}: {e}")
            raise e

# Wrapper classes for easy instantiation
class BMIAdvisor(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "BMIAdvisor")

class Generalist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Generalist")

class Emergency(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Emergency")

class Cardiologist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Cardiologist")

class Pulmonologist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Pulmonologist")

class Gastroenterologist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Gastroenterologist")

class Neurologist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Neurologist")

class Endocrinologist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Endocrinologist")

class Surgeon(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Surgeon")

class OBGYN(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "OBGYN")

class Pediatrician(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Pediatrician")

class ENT(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "ENT")

class Dermatologist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Dermatologist")

class Ophthalmologist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Ophthalmologist")

class Dentist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Dentist")

class Psychiatrist(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "Psychiatrist")

class MultidisciplinaryTeam(Agent):
    def __init__(self, specialist_reports):
        super().__init__(role="MultidisciplinaryTeam", extra_info={"specialist_reports": specialist_reports})

class Consultant(Agent):
    def __init__(self, diagnosis_context, consultant_type, chat_history, user_question):
        super().__init__(
            medical_report=user_question, 
            role="Consultant", 
            extra_info={
                "diagnosis_context": diagnosis_context,
                "consultant_type": consultant_type,
                "chat_history": chat_history
            }
        )

class TreatmentPlanner(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "TreatmentPlanner")

class PharmacogenomicsAdvisor(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "PharmacogenomicsAdvisor")

class DiagnosticExplainer(Agent):
    def __init__(self, medical_report): super().__init__(medical_report, "DiagnosticExplainer")
