# Kết quả ARM — đọc theo ba bước

1. **1_train**: bốn bảng luật được sinh từ Train; có chỉ số Val tính sẵn để bước sau xét cấu hình.
2. **2_validation**: bốn bảng luật được chọn bằng Validation, có cấu hình chung và thứ tự báo cáo theo Val.
3. **3_test**: bốn bảng đánh giá toàn bộ luật đã chọn, cộng `summary.csv` đếm số luật qua từng bước.

H1/H5/H10/H20 là số phiên Gold tới ngày đích. Không xóa luật yếu ở Test: giữ lại và đánh dấu để thấy luật nào không duy trì hiệu quả.

Chạy bốn notebook `notebook/ARM/ARM-H*/arm_h*.ipynb`, sau đó `ARM-FINAL/arm_test.ipynb`. `arm_rule_discovery.ipynb` đọc ba thư mục này, tính bảng tổng hợp và vẽ biểu đồ trực tiếp, không sinh báo cáo phụ.

Các ngưỡng encoding và thông tin cần tái lập nằm cùng dữ liệu tại `data/arm/ARM-H*/train_encoding.pkl`, không phải báo cáo để đọc. README viết thủ công. Bảng grid, nhật ký purge và số itemset được hiển thị trong notebook.
