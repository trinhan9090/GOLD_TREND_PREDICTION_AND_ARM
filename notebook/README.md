# Notebook — quy trình chạy chính

`00_prepare_data.ipynb` tạo feature, ghép lịch, target. 
`01_verify_project.ipynb` kiểm chứng, không train. 
`EDA` giữ 4 phân tích cũ. 
`Classification` chứa A/B của 4 horizon và code train trực tiếp. 
`ARM` chứa bốn notebook khai phá Train/Val, ARM-FINAL/arm_test.ipynb chọn config/khóa luật/Test và arm_rule_discovery.ipynb phân tích ba chỉ số.

Không cần chạy EDA để train. Đã có dữ liệu thì có thể mở thẳng model. Classification Run All train lại; ARM chạy đủ bốn horizon trước FINAL. Mỗi notebook tự tìm ROOT qua project_manifest.json, không cần file helper model trong src. README gốc giải thích split khác nhau giữa RF/LR và RNN/LSTM.
