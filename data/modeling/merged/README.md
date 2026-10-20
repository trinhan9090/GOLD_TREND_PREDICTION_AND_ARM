# Ghép dữ liệu theo lịch

`date_cleaned_dataset.csv`: bảng lịch hợp, raw/feature/nguồn ngày và cờ carry-forward. `modeling_dataset.csv`: 5.458 phiên Gold, 11 feature và nhãn H1 0/1, chưa scale. `candidate_features.csv`: danh sách chính thức 11 feature, không phải kết quả chọn tương quan.

`alignment_logs` ghi ngày thiếu Gold, nguồn dùng carry-forward, điều kiện giữ mẫu và target H1. Giữ thư mục này vì phản ánh xử lý lịch thực tế, không phải audit chọn feature của pipeline cũ. Target đa horizon nằm riêng ở `../horizons`.
