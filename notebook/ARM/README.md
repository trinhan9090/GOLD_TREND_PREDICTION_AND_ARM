# ARM — thực thi trong notebook

Chạy ARM-H1, ARM-H5, ARM-H10, ARM-H20 (bất kỳ thứ tự, đủ cả bốn), sau đó ARM-FINAL/arm_test.ipynb, cuối cùng ARM-FINAL/arm_rule_discovery.ipynb. Các notebook horizon fit ngưỡng Train, chạy Apriori, tính Val và hiển thị 27 cấu hình; chỉ lưu một bảng ứng viên mỗi horizon tại `results/arm/1_train`. arm_test chọn cấu hình chung, lưu luật đã chốt tại `2_validation`, đánh giá tại `3_test`. arm_rule_discovery đọc kết quả, vẽ biểu đồ và xếp hạng, không sinh thêm báo cáo.

Tất cả code nằm trong các cell, không gọi src/arm_horizons.py. Run All thực sự tính lại và cập nhật data/arm, results/arm. Không chỉnh grid theo Test sau khi đã xem Test. Cấu hình hiện tại 0.02/0.50/1.00 và ngưỡng encoding riêng từng Train được giữ nguyên.
