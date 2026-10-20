# Transaction H1

ARM_train/val/test.csv là item có nghĩa; các file cùng tên hậu tố _onehot.csv là 35 cột 0/1 và ngày. Train 4.020, Val 753, Test 683. Consequent Gold_Up_H1/Gold_NonUp_H1. Dữ liệu nguồn data/modeling/horizons/h1. Không scale/window.

`train_encoding.pkl`: ngưỡng đã fit trên Train, số frequent itemset theo độ dài và thông tin/hash dữ liệu nguồn. Notebook ARM-H1 tạo artifact này; ARM Test đọc lại để áp dụng đúng encoding đã học, không fit trên Test. Có thể xem ngưỡng ngay trong output notebook.
