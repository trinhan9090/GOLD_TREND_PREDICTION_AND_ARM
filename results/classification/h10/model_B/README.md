# H10 — B: 11 feature Gold và thị trường ngoài

Nguồn: `notebook/Classification/H10/classification_B.ipynb`.

Mỗi tên `Naive`, `RandomForest`, `LogisticRegression`, `RNN`, `LSTM` có hai file: `_model_and_scaler.pkl` chứa model/scaler/cấu hình; `_test_predictions.csv` chứa ngày, ngày đích, nhãn thật, xác suất Up và nhãn dự đoán. Up=1, NonUp=0, ngưỡng 0,5. So sánh chỉ số trong `../../test_model_comparison.csv`. Không fit lại scaler khi dùng model đã lưu.
