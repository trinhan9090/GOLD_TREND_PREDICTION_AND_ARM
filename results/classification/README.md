# Kết quả Classification

Mở **test_model_comparison.csv** trước: một bảng chung cho H1/H5/H10/H20 × A/B × Naive/Random Forest/Logistic Regression/RNN/LSTM.

- `Horizon`: số phiên Gold tới ngày đích; `Variant`: A = 7 feature Gold, B = 11 feature.
- `Model`: Naive, RF (Random Forest), LR (Logistic Regression), RNN hoặc LSTM.
- `ROC_AUC`, `Macro_F1`, `Accuracy`, `Balanced_Accuracy`: cao hơn thường tốt hơn.
- `Log_Loss`, `Brier_Score`, `ECE_10`: thấp hơn thường tốt hơn. ECE dùng 10 khoảng xác suất; chưa hiệu chỉnh xác suất.
- `Pred_Up`, `Pred_Non_Up`: số dự đoán hai lớp; `Rows`: số mẫu Test.

Trong `h1`, `h5`, `h10`, `h20`, mỗi bộ `model_A`/`model_B` chỉ có hai file cho mỗi thuật toán:

| Tên file | Nội dung |
|---|---|
| `<ThuậtToán>_model_and_scaler.pkl` | Model đã học (hoặc state_dict của RNN/LSTM), scaler riêng và cấu hình/feature/thông tin checkpoint. |
| `<ThuậtToán>_test_predictions.csv` | Date, Target_Date, Actual, Probability_Up, Predicted của đúng model trên Test. |

Tên thuật toán trong file được viết đầy đủ: `Naive`, `RandomForest`, `LogisticRegression`, `RNN`, `LSTM`.

Artifact pickle là dictionary có `scaler`, `configuration`, và `model` cho thuật toán tabular hoặc `state_dict` cho mạng. Nạp mạng bằng lớp `SequenceClassifier` trong notebook và `load_state_dict`. `01_verify_project.ipynb` có ví dụ nạp lại cả 40 artifact và kiểm tra dự đoán.

Notebook classification tương ứng tạo các file này và cập nhật đúng horizon/bộ feature trong bảng chung. Chạy tuần tự các notebook khi cập nhật cùng bảng chung. Không lưu CSV calibration, lịch sử train, metrics từng model hoặc dự đoán Train/Val: các bảng đó hiển thị trong notebook; calibration tính lại từ xác suất Test.

Naive lấy lớp phổ biến của Train. RF/LR học 2005–2023; RNN/LSTM học 2005–2020, dùng Val 2021–2023 cho early stopping. Test bắt đầu 2024, cùng ngày giữa các thuật toán. Purge nhãn vượt biên và scaler chỉ fit Train giữ nguyên.
