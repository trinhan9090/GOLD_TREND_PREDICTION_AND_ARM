# Target theo horizon

`h1`, `h5`, `h10`, `h20` giữ cùng ngày t và 11 feature, chỉ đổi target theo Close sau h phiên Gold. Mỗi thư mục có modeling_dataset.csv và target_trace.csv. Target được tạo trên lịch Gold gốc. Purge endpoint vượt biên Train/Val được thực hiện trong notebook model/ARM, không xóa khỏi dữ liệu nguồn.
