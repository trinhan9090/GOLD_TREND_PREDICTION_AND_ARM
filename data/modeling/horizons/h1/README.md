# H1 — dữ liệu chưa scale

`modeling_dataset.csv`: Date, 11 feature và Gold_Target_Next cho 5.458 phiên. `target_trace.csv`: Date/Close, Target_Date/Target_Close, nhãn và Horizon=1. Up nếu phiên Gold tiếp theo cao hơn, NonUp gồm giảm/đứng giá. Dùng chung cho classification và ARM H1; notebook tự chia tập/purge.
