# H10 — dữ liệu chưa scale

`modeling_dataset.csv`: Date, 11 feature và Gold_Target_Next cho 5.458 phiên. `target_trace.csv`: Date/Close, Target_Date/Target_Close, nhãn và Horizon=10. Up nếu giá sau 10 phiên Gold cao hơn, NonUp gồm giảm/đứng giá. Dùng chung cho classification và ARM H10; notebook tự chia tập/purge.
