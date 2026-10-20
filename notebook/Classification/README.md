# Classification đa horizon

H1/H5/H10/H20 có classification_A.ipynb (7 feature Gold) và classification_B.ipynb (11 feature). Mỗi notebook có đầy đủ code Naive/RF/LR/RNN/LSTM, scaler, window, train và đánh giá. Run All thực sự huấn luyện lại, ghi đúng nhánh results/classification/h*/model_A hoặc model_B. Không import thuật toán từ src.

Mỗi thuật toán lưu `<Tên>_model_and_scaler.pkl` và `<Tên>_test_predictions.csv` trực tiếp trong nhánh A/B. Artifact chứa mô hình đã học, scaler và cấu hình tương ứng. Bảng `results/classification/test_model_comparison.csv` tổng hợp chỉ số Test của 40 lượt mô hình.

Calibration, lịch sử early stopping và thống kê purge được hiển thị trong output notebook, không tạo CSV riêng. `01_verify_project.ipynb` nạp lại checkpoint và đối chiếu dự đoán Test. Các notebook cập nhật bảng chung tuần tự theo horizon và A/B.
