# Nhật ký căn chỉnh lịch

- `calendar_alignment.csv`: ngày quan sát, Source_Date và độ tuổi dữ liệu mỗi nguồn.
- `forward_fill_log.csv`: từng giá trị được mang từ phiên nguồn gần nhất trong quá khứ.
- `dates_without_gold.csv`: ngày có nguồn khác nhưng raw Gold không có; vẫn giữ trong lịch hợp, không tự điền Gold/nhãn.
- `model_eligibility.csv`: ngày đủ điều kiện thành mẫu modeling và lý do loại.
- `gold_target_trace.csv`: giá/ngày kế tiếp dùng tạo H1, bao gồm đứng giá.
- `summary.json`: số mẫu, policy, hash raw và thống kê lịch.

Nguồn: notebook chuẩn bị dữ liệu. Không khẳng định ngày thiếu là ngày sàn đóng cửa; có thể do lịch hoặc nguồn crawl.
