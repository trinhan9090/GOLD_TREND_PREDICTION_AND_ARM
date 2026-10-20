# Gold Direction Forecasting & Association Rule Mining

Đây là repository nộp bài cuối kỳ môn **Khai phá dữ liệu và Khai phá tri thức** tại **Trường Đại học Tôn Đức Thắng**.

Dự án nghiên cứu bài toán **dự đoán hướng biến động giá vàng theo nhiều khoảng dự báo** và **khai phá các luật liên hệ giữa Gold, Oil, Dollar Index và S&P 500**. Hệ thống được xây dựng theo hai nhánh chính:

1. **Classification theo horizon**: dự đoán Gold **Up / NonUp** sau 1, 5, 10 và 20 phiên.
2. **Association Rule Mining (ARM) theo horizon**: tìm các tổ hợp trạng thái thị trường có liên hệ với hướng Gold trong tương lai và kiểm tra mức độ ổn định của các luật trên Train → Validation → Test.

Mục tiêu của dự án không phải xây dựng một hệ thống giao dịch tự động, mà là kiểm tra:

- khả năng dự đoán hướng giá vàng ở nhiều horizon;
- việc bổ sung thông tin từ Oil, Dollar Index và S&P 500 có giúp mô hình tổng quát hóa tốt hơn hay không;
- các mối liên hệ giữa nhiều thị trường có ổn định qua thời gian và qua các horizon hay không.

---

## Thành viên nhóm

| MSSV | Họ và tên | Phân công chính |
|---|---|---|
| 52300138 | Nguyễn Trí Nhân | Association Rule Mining, tổng hợp pipeline, phân tích kết quả ARM, hỗ trợ báo cáo và tích hợp hệ thống |
| 52300088 | Lê Hoài An | Classification, thực nghiệm mô hình học máy/học sâu và phân tích kết quả dự đoán |

> Phân công trên mô tả phần phụ trách chính; các phần chuẩn bị dữ liệu, kiểm tra kết quả và hoàn thiện báo cáo được phối hợp chung.

---

# 1. Bài toán nghiên cứu

## 1.1. Classification theo horizon

Tại một phiên Gold \(t\), nhãn được xác định bằng:

```text
Up     nếu Close(t + H) > Close(t)
NonUp  nếu Close(t + H) <= Close(t)
```

với:

```text
H ∈ {1, 5, 10, 20}
```

Do đó dự án có bốn bài toán phân loại:

```text
H1  : hướng Gold sau 1 phiên
H5  : hướng Gold sau 5 phiên
H10 : hướng Gold sau 10 phiên
H20 : hướng Gold sau 20 phiên
```

`NonUp` bao gồm cả trường hợp giảm và đứng giá.

Việc sử dụng nhiều horizon giúp kiểm tra xem khả năng dự đoán có thay đổi khi khoảng dự báo dài hơn hay không, thay vì chỉ xét phiên kế tiếp.

---

## 1.2. Association Rule Mining theo horizon

ARM trả lời một câu hỏi khác:

> **Có những tổ hợp trạng thái thị trường nào tại phiên hiện tại thường đi cùng với việc Gold Up hoặc NonUp sau H phiên hay không?**

Ví dụ:

```text
Gold_RSI_14 = Medium
AND Oil_Price_Change = Positive
AND SP500_Daily_Return = Negative
→ Gold_NonUp_H5
```

Trong tài liệu của dự án:

- **Tiền đề**: các điều kiện ở bên trái của luật.
- **Hậu quả**: kết quả Gold Up hoặc NonUp ở bên phải.
- ARM chỉ mô tả **mối liên hệ thống kê**, không chứng minh quan hệ nhân quả.

ARM được sử dụng như một nhánh **giải thích bổ sung** cho Classification. Nếu Model B có thêm biến thị trường bên ngoài nhưng không luôn tốt hơn Model A, ARM giúp kiểm tra liệu các biến đó có chỉ hữu ích trong **một số trạng thái cụ thể** và liệu các mối liên hệ đó có giữ được trên dữ liệu mới hay không.

---

# 2. Nguồn dữ liệu

Dự án sử dụng dữ liệu tài chính tần suất ngày từ Yahoo Finance:

| Nguồn | Mã |
|---|---|
| Gold Futures | `GC=F` |
| Crude Oil Futures | `CL=F` |
| U.S. Dollar Index | `DX-Y.NYB` |
| S&P 500 | `^GSPC` |

Các snapshot EDA chính bao phủ khoảng **2010–2026**.

Trong modelling, dữ liệu lịch sử được mở rộng về trước để tăng lượng mẫu Train. Phần lịch sử bổ sung chỉ phục vụ huấn luyện; Validation và Test vẫn nằm ở các giai đoạn sau theo thứ tự thời gian.

### Lưu ý về phạm vi EDA và modelling

EDA tập trung vào giai đoạn nghiên cứu chính **2010–2026**, trong khi modelling tận dụng thêm dữ liệu lịch sử trước 2010 để tăng số quan sát huấn luyện.

Hai phạm vi này phục vụ hai mục đích khác nhau:

- **EDA**: mô tả cấu trúc và hành vi dữ liệu trong giai đoạn nghiên cứu chính.
- **Modelling**: tận dụng thêm lịch sử để mô hình học được nhiều trạng thái thị trường hơn.

Phần dữ liệu lịch sử bổ sung chỉ nằm trong Train và không làm thay đổi Validation/Test.

---

# 3. Xử lý và đồng bộ dữ liệu

Các feature được tính trên **lịch giao dịch gốc của từng nguồn trước khi gộp**.

Khi một thị trường bên ngoài không có phiên tại ngày Gold đang giao dịch:

- sử dụng giá trị từ phiên gần nhất trước đó;
- không lấy dữ liệu tương lai;
- không nội suy;
- không tính lại return trên giá đã được mang sang.

Gold không được điền giả.

Các ngày không có phiên Gold có thể được giữ để truy vết lịch nhưng không được dùng làm mẫu modelling.

Đối với các horizon dài hơn, các mẫu ở cuối Train hoặc Validation có ngày hậu quả rơi sang tập tiếp theo được loại khỏi tập hiện tại. Bước này được gọi là **purging**, nhằm tránh việc nhãn tương lai vượt qua ranh giới Train/Validation/Test.

---

# 4. Hai nhóm đặc trưng Classification

## Model A — Gold-only

Model A sử dụng 7 đặc trưng chỉ từ Gold:

1. `Gold_Daily_Return`
2. `Gold_Return_Lag_1`
3. `Gold_Intraday_Range`
4. `Gold_Volatility_20`
5. `Gold_Distance_to_MA_20`
6. `Gold_RSI_14`
7. `Gold_MACD_Histogram`

Mục tiêu:

> Kiểm tra khả năng dự đoán chỉ từ thông tin nội tại của Gold.

---

## Model B — Gold + External Markets

Model B giữ 7 đặc trưng của Model A và bổ sung:

8. `Oil_Price_Change`
9. `Dollar_Daily_Return`
10. `SP500_Daily_Return`
11. `SP500_Drawdown`

Mục tiêu:

> Kiểm tra việc bổ sung Oil, Dollar Index và S&P 500 có cải thiện khả năng dự đoán và tổng quát hóa hay không.

---

# 5. Các mô hình Classification

Các mô hình được so sánh gồm:

- **Naive baseline**
- **Logistic Regression**
- **Random Forest**
- **RNN**
- **LSTM**

Mỗi mô hình được đánh giá trên:

```text
4 horizons × 2 feature sets
```

Hai feature set:

```text
A = Gold-only
B = Gold + external markets
```

Naive luôn dự đoán lớp chiếm đa số và được dùng làm mốc tham chiếu.

---

# 6. Chia dữ liệu theo thời gian

Dữ liệu không được shuffle ngẫu nhiên vì đây là dữ liệu chuỗi thời gian.

Thiết kế thực nghiệm hiện tại sử dụng:

```text
Train      : giai đoạn lịch sử đầu
Validation : 2021–2023 đối với pipeline ARM/RNN-LSTM hiện tại
Test       : 02/01/2024–18/09/2026
```

Tập Test chung có **683 phiên Gold** cho bốn horizon.

Đối với ARM sau bước purge:

| Horizon | Train | Validation | Test |
|---|---:|---:|---:|
| H1 | 4,020 | 753 | 683 |
| H5 | 4,016 | 749 | 683 |
| H10 | 4,011 | 744 | 683 |
| H20 | 4,001 | 734 | 683 |

Số mẫu Train/Validation giảm nhẹ khi horizon tăng vì cần loại các mẫu có ngày hậu quả vượt sang tập tiếp theo.

---

# 7. Đánh giá Classification

Các chỉ số chính:

- **Balanced Accuracy**
- **Macro-F1**
- **ROC-AUC**

Các chỉ số bổ sung:

- Accuracy
- Log Loss
- Brier Score
- Expected Calibration Error (ECE)

Accuracy không được sử dụng một mình vì lớp `Up` chiếm ưu thế ở cả bốn horizon. Tỷ lệ Up nhìn chung cao hơn ở horizon dài nhưng không tăng đơn điệu: H1 56,22%; H5 61,79%; H10 61,20%; H20 66,91%. Ở H20, lớp Up chiếm phần lớn tập Test, nên một mô hình chỉ dự đoán Up cũng có thể đạt Accuracy cao nhưng Balanced Accuracy gần 0.5.

---

# 8. Kết quả Classification tổng quát

Kết quả cho thấy không có một mô hình hoặc một feature set luôn thắng ở mọi horizon.

Một số điểm chính:

- H1 có tín hiệu tương đối yếu.
- Một số cấu hình ở H5 và H20 đạt Balanced Accuracy/Macro-F1 tốt hơn.
- Model B không cải thiện nhất quán so với Model A.
- Một số mô hình có hiện tượng nghiêng mạnh về lớp đa số.
- Hiệu năng không tăng đều khi horizon dài hơn.

Do đó kết luận phù hợp là:

> **Thông tin từ các thị trường bên ngoài có thể hữu ích trong một số horizon hoặc mô hình, nhưng không tạo ra cải thiện ổn định trên toàn bộ bài toán.**

---

# 9. Vì sao dùng ARM?

Kết quả Classification đặt ra câu hỏi:

> Nếu Oil, Dollar và S&P 500 không luôn giúp Model B tốt hơn Model A, liệu chúng có thực sự không chứa thông tin liên quan đến Gold?

ARM được dùng để kiểm tra sâu hơn.

Thay vì hỏi:

> “External features có giúp classifier tốt hơn không?”

ARM hỏi:

> “External features có tạo ra những tổ hợp trạng thái cụ thể liên hệ với Gold Up/NonUp hay không?”

Điều này giúp phân biệt:

- **thông tin hữu ích toàn cục**, có thể giúp classifier ổn định;
- và **thông tin phụ thuộc điều kiện**, chỉ xuất hiện trong một số trạng thái thị trường.

---

# 10. Chuẩn bị dữ liệu cho ARM

ARM không sử dụng trực tiếp các giá trị liên tục như:

```text
RSI = 47.3
Dollar Return = -0.002
Volatility = 0.013
```

Các giá trị được chuyển thành trạng thái.

## Các feature theo dấu

```text
Negative / Zero / Positive
```

Áp dụng cho:

- Gold Daily Return
- Gold Return Lag 1
- Gold Distance to MA20
- Gold MACD Histogram
- Oil Price Change
- Dollar Daily Return
- S&P 500 Daily Return

## Các feature theo mức độ

```text
Low / Medium / High
```

Áp dụng cho:

- Gold Intraday Range
- Gold Volatility 20
- Gold RSI14

Ngưỡng được xác định bằng quantile 1/3 và 2/3 trên **Train của từng horizon**.

## S&P 500 Drawdown

```text
Deep / Medium / Shallow
```

cũng dùng quantile 1/3 và 2/3.

Ngưỡng học từ Train được giữ nguyên khi áp dụng sang Validation và Test.

---

# 11. Quy trình Apriori

Sau khi chuyển thành trạng thái, mỗi phiên trở thành một tập trạng thái.

Ví dụ:

```text
Gold_RSI_14=Medium
Gold_Volatility_20=High
Oil_Price_Change=Positive
Dollar_Daily_Return=Negative
SP500_Daily_Return=Negative
Gold_NonUp_H5
```

Apriori tìm các **tổ hợp trạng thái xuất hiện đủ thường xuyên**.

Trong dự án:

```text
min_support ban đầu = 0.02
max itemset size    = 4
```

Sau đó sinh luật dạng:

```text
Tiền đề → Hậu quả
```

với:

- tiền đề gồm 1–3 trạng thái;
- hậu quả đúng một nhãn Gold Up hoặc NonUp;
- nhãn tương lai không được xuất hiện trong tiền đề.

Ví dụ:

```text
Gold_RSI_14=Medium
AND Oil_Price_Change=Positive
AND SP500_Daily_Return=Negative
→ Gold_NonUp_H5
```

---

# 12. Support, Confidence và Lift

## Support — độ phổ biến của toàn bộ luật

```text
Support =
số phiên có cả tiền đề và hậu quả
/
tổng số phiên
```

Support cao nghĩa là tổ hợp xuất hiện tương đối thường xuyên.

---

## Confidence — tỷ lệ hậu quả khi tiền đề xuất hiện

```text
Confidence =
số phiên có cả tiền đề và hậu quả
/
số phiên có tiền đề
```

Ví dụ Confidence = 0.70 nghĩa là trong những phiên có tiền đề, 70% trường hợp xuất hiện hậu quả.

---

## Lift — mức liên hệ so với tỷ lệ nền

```text
Lift =
Confidence
/
tỷ lệ nền của hậu quả
```

Cách đọc:

```text
Lift > 1 : hậu quả xuất hiện nhiều hơn mức nền
Lift = 1 : gần mức nền
Lift < 1 : hậu quả xuất hiện ít hơn mức nền
```

Lift đặc biệt quan trọng vì tỷ lệ Gold Up/NonUp thay đổi theo horizon.

Một Confidence cao chưa chắc là một luật mạnh nếu hậu quả vốn đã xảy ra rất thường xuyên.

---

# 13. Train → Validation → Test của ARM

Đây là phần quan trọng nhất của nhánh ARM.

## Bước 1 — Train: tìm luật ứng viên

Với từng horizon:

```text
Train
↓
học ngưỡng rời rạc hóa
↓
chuyển mỗi phiên thành các trạng thái
↓
Apriori tìm tổ hợp thường xuyên
↓
sinh luật ứng viên
↓
tính Support / Confidence / Lift trên Train
```

Số luật ứng viên:

| Horizon | Luật ứng viên Train |
|---|---:|
| H1 | 4,374 |
| H5 | 4,341 |
| H10 | 4,328 |
| H20 | 4,335 |

---

## Bước 2 — 27 bộ ngưỡng lọc luật

Nhóm định nghĩa trước:

```text
Support    ∈ {0.02, 0.05, 0.10}
Confidence ∈ {0.50, 0.55, 0.60}
Lift       ∈ {1.00, 1.05, 1.10}
```

Số cấu hình:

```text
3 × 3 × 3 = 27
```

Các bộ ngưỡng này:

- không sinh ngẫu nhiên;
- không được Apriori tự học;
- không được Test quyết định.

Đây là **lưới tham số được định nghĩa trước** để thử nhiều mức lọc khác nhau.

Có thể xem chúng như 27 “cái rây” có độ chặt khác nhau cùng lọc một tập luật ứng viên.

---

## Bước 3 — Validation: chọn bộ ngưỡng

Validation không tìm luật mới.

Các luật được tìm từ Train được tính lại trên Validation.

Một luật được xem là **ổn định** khi:

```text
số lần tiền đề xuất hiện trên Validation ≥ 30
AND
Lift Validation > 1
```

Có:

```text
4 horizon × 2 hướng = 8 nhóm
```

gồm:

```text
H1-Up
H1-NonUp
H5-Up
H5-NonUp
H10-Up
H10-NonUp
H20-Up
H20-NonUp
```

Một cấu hình chỉ hợp lệ nếu cả 8 nhóm đều còn ít nhất một luật ổn định.

Trong từng nhóm:

```text
lấy median Lift Validation
```

Sau đó:

```text
Score của cấu hình =
Mean của 8 median Lift
```

Cấu hình có Score cao nhất được chọn.

---

## Cấu hình ARM được chọn

```text
min_support    = 0.02
min_confidence = 0.50
min_lift       = 1.00
```

Validation score:

```text
1.087585
```

Sau khi chọn cấu hình, danh sách luật được khóa trước khi đánh giá Test.

---

# 14. Các luật được chốt

| Horizon | Luật chốt |
|---|---:|
| H1 | 835 |
| H5 | 476 |
| H10 | 442 |
| H20 | 536 |
| **Tổng** | **2,289** |

Trong đó có **1,743 lượt luật chứa ít nhất một trạng thái từ Oil, Dollar hoặc S&P 500**.

Không có luật mới được sinh từ Test.

---

# 15. Test — kiểm tra khả năng giữ hiệu lực trên dữ liệu mới

Toàn bộ **2,289 luật đã chốt** được đem sang Test.

Với từng luật, Test chỉ:

1. đếm số lần tiền đề xuất hiện;
2. đếm số lần tiền đề và hậu quả cùng xuất hiện;
3. tính lại Support;
4. tính lại Confidence;
5. tính lại Lift.

Test không được dùng để:

- thay đổi cấu hình;
- thêm luật;
- bỏ luật xấu;
- chọn lại rule set.

---

# 16. Kết quả ARM trên Test

Trong 2,289 luật:

| Kết quả | Số luật | Tỷ lệ |
|---|---:|---:|
| Lift > 1 và tiền đề xuất hiện ≥30 lần | **1,042** | **45.5%** |
| Lift > 1 nhưng tiền đề xuất hiện <30 lần | 238 | 10.4% |
| Lift ≤ 1 | 990 | 43.3% |
| Không tính được Lift | 19 | 0.8% |

Có thể diễn giải:

> Gần một nửa số luật được Train phát hiện và Validation chấp nhận vẫn giữ được Lift > 1 với số lần xuất hiện đủ lớn trên Test.

Điều này **không có nghĩa 1,042 luật đã được chứng minh đúng**. Đây chỉ là những luật còn giữ liên hệ dương theo tiêu chí mô tả của dự án.

---

# 17. ARM theo horizon

Median Test Lift của các luật external:

| Horizon | Gold Up | Gold NonUp |
|---|---:|---:|
| H1 | 1.021 | 1.028 |
| H5 | **1.036** | 0.945 |
| H10 | 1.012 | 0.953 |
| H20 | 0.956 | 0.948 |

Nhận xét:

- H1: liên hệ còn nhẹ ở cả hai hướng.
- H5: nhóm Up có mức liên hệ tổng thể tốt nhất.
- H10: Up còn rất nhẹ, NonUp suy giảm.
- H20: cả Up và NonUp đều có median Lift dưới 1.

Kết quả cho thấy:

> **Mối liên hệ giữa các thị trường không mạnh lên đều khi horizon tăng.**

---

# 18. Một ví dụ luật giữ được tốt

H5 — NonUp:

```text
Gold_RSI_14=Medium
AND Oil_Price_Change=Positive
AND SP500_Daily_Return=Negative
→ Gold_NonUp_H5
```

Kết quả:

```text
Validation Lift ≈ 1.259
Test antecedent count = 64
Test joint count = 31
Test Confidence ≈ 0.484
Test Lift ≈ 1.268
```

Luật này giữ được mức liên hệ tốt khi chuyển từ Validation sang Test.

---

# 19. Một ví dụ luật không tổng quát hóa tốt

H5 — Up:

```text
Gold_Volatility_20=High
AND SP500_Daily_Return=Positive
AND SP500_Drawdown=Shallow
→ Gold_Up_H5
```

Kết quả:

```text
Validation Lift ≈ 1.442
Test antecedent count = 123
Test joint count = 61
Test Confidence ≈ 0.496
Test Lift ≈ 0.803
```

Một luật rất mạnh trên Validation có thể mất liên hệ khi sang Test.

Điều này cho thấy các quan hệ thị trường có thể **thay đổi theo thời gian và theo trạng thái thị trường**.

---

# 20. Liên hệ giữa Classification và ARM

Hai nhánh không cạnh tranh với nhau mà trả lời hai câu hỏi khác nhau.

### Classification

> Các feature hiện tại có giúp mô hình dự đoán hướng Gold ngoài mẫu hay không?

### ARM

> Có những trạng thái cụ thể nào liên hệ với Gold Up/NonUp và các mối liên hệ này có bền qua thời gian hay không?

Kết hợp hai nhánh:

> Model B không luôn tốt hơn Model A, nhưng ARM vẫn tìm thấy nhiều cross-market association trong một số điều kiện cụ thể.

Tuy nhiên, nhiều luật suy giảm từ Validation sang Test.

Điều này gợi ý:

> **Thông tin external có tính phụ thuộc điều kiện và không ổn định hoàn toàn theo thời gian, thay vì luôn cung cấp tín hiệu dự báo mạnh.**

Dự án không xây Model C từ luật ARM. ARM được giữ như một nhánh phân tích giải thích bổ sung cho kết quả Classification.

---

# 21. Market regime và sự thay đổi quan hệ theo thời gian

Trong báo cáo, “market regime” nên hiểu là:

> **Bối cảnh vận hành của thị trường trong một giai đoạn**, ví dụ trạng thái biến động cao/thấp, xu hướng tăng/giảm, drawdown sâu/nông hoặc cấu trúc quan hệ giữa Gold và các thị trường khác.

Nhiều luật có Lift tốt trên Train/Validation nhưng giảm mạnh trên Test.

Kết quả này **không chứng minh trực tiếp rằng đã xảy ra regime shift**, vì dự án không xây thuật toán phát hiện regime.

Cách diễn giải phù hợp hơn:

> Sự suy giảm của nhiều luật khi chuyển sang Test cho thấy các mối liên hệ thị trường không ổn định hoàn toàn theo thời gian và có thể phụ thuộc vào trạng thái thị trường.

---

# 22. Cấu trúc repository

Cấu trúc chính của dự án được tổ chức theo các tầng dữ liệu, notebook và kết quả:

```text
PROJECT_FINAL/
├── README.md
│
├── data/
│   ├── eda_2010_2026/
│   ├── arm/ARM-H1,ARM-H5,ARM-H10,ARM-H20/
│   └── modeling/
│       ├── raw/
│       ├── support/
│       ├── provenance/
│       ├── features/
│       ├── merged/alignment_logs/
│       └── horizons/h1,h5,h10,h20/
│
├── notebook/
│   ├── 00_prepare_data.ipynb
│   ├── 01_verify_project.ipynb
│   ├── EDA/
│   ├── Classification/H1,H5,H10,H20/
│   └── ARM/
│       ├── ARM-H1/
│       │   └── arm_h1.ipynb
│       ├── ARM-H5/
│       │   └── arm_h5.ipynb
│       ├── ARM-H10/
│       │   └── arm_h10.ipynb
│       ├── ARM-H20/
│       │   └── arm_h20.ipynb
│       └── ARM-FINAL/
│           ├── arm_test.ipynb
│           └── arm_rule_discovery.ipynb
│
├── results/
│   ├── classification/
│   │   ├── test_model_comparison.csv
│   │   └── h1,h5,h10,h20/model_A,model_B/
│   │       ├── <algorithm>_model_and_scaler.pkl
│   │       └── <algorithm>_test_predictions.csv
│   └── arm/
│       ├── 1_train/
│       ├── 2_validation/
│       └── 3_test/
│
└── src/
    └── crawl/download_snapshot.py
```

Mỗi bước ARM có một bảng luật cho từng horizon; `3_test/summary.csv` tổng hợp số luật qua ba bước. Classification có hai file cho mỗi thuật toán, cùng một bảng so sánh chung. Calibration và các bảng trung gian được hiển thị trong notebook.

---

# 23. Vai trò của các notebook ARM

| Notebook | Vai trò |
|---|---|
| `ARM-H1/arm_h1.ipynb` | Khai phá Train và đánh giá Validation cho H1 |
| `ARM-H5/arm_h5.ipynb` | Khai phá Train và đánh giá Validation cho H5 |
| `ARM-H10/arm_h10.ipynb` | Khai phá Train và đánh giá Validation cho H10 |
| `ARM-H20/arm_h20.ipynb` | Khai phá Train và đánh giá Validation cho H20 |
| `ARM-FINAL/arm_test.ipynb` | So sánh 27 cấu hình, chọn cấu hình chung, khóa luật và đánh giá Test |
| `ARM-FINAL/arm_rule_discovery.ipynb` | Phân tích Support, Confidence, Lift và trực quan hóa các luật đã được đánh giá |

`arm_rule_discovery.ipynb` chỉ phân tích kết quả sau Test; nó không mine lại từ Test và không đặt thêm ngưỡng để chọn luật mới.

---

# 24. Quy trình chạy tổng quát

```text
Raw data
↓
Kiểm tra và làm sạch
↓
Feature Engineering
↓
Đồng bộ lịch giao dịch
↓
Tạo nhãn H1 / H5 / H10 / H20
↓
Chia Train / Validation / Test theo thời gian
↓
┌──────────────────────────────┬──────────────────────────────┐
│        CLASSIFICATION        │             ARM              │
│                              │                              │
│ Model A / Model B            │ Rời rạc hóa trạng thái       │
│ Naive / LR / RF / RNN / LSTM│ Apriori trên Train           │
│ Validation                   │ 27 bộ ngưỡng                 │
│ Test                         │ Validation chọn cấu hình     │
│                              │ Khóa luật                    │
│                              │ Test luật                    │
└──────────────────────────────┴──────────────────────────────┘
↓
So sánh kết quả
↓
Phân tích khả năng tổng quát hóa và quan hệ cross-market
```

---

# 25. Cách chạy lại dự án

Quy trình cụ thể phụ thuộc vào môi trường và phiên bản notebook trong repository.

Luồng chung:

1. Snapshot đã lưu tại `data/modeling/raw`, `data/modeling/support` và `data/eda_2010_2026`.
2. `notebook/00_prepare_data.ipynb` xử lý dữ liệu để:
   - tính feature;
   - đồng bộ lịch;
   - tạo target;
   - tạo dữ liệu theo horizon.
3. Chạy các notebook EDA.
4. Chạy Classification cho H1/H5/H10/H20 với Model A và Model B.
5. Chạy lần lượt:
   - `ARM-H1/arm_h1.ipynb`
   - `ARM-H5/arm_h5.ipynb`
   - `ARM-H10/arm_h10.ipynb`
   - `ARM-H20/arm_h20.ipynb`
6. Sau khi bốn horizon hoàn tất, chạy:
   - `ARM-FINAL/arm_test.ipynb`
7. Cuối cùng chạy:
   - `ARM-FINAL/arm_rule_discovery.ipynb`

Không chạy `arm_rule_discovery.ipynb` để chọn lại luật dựa trên Test.

---

# 26. Các thư viện Python chính

Dự án sử dụng chủ yếu:

- `numpy`
- `pandas`
- `matplotlib`
- `scikit-learn`
- thư viện hỗ trợ mô hình RNN/LSTM trong notebook thực nghiệm
- các thư viện chuẩn Python phục vụ lưu kết quả, kiểm tra và tái lập pipeline

Phiên bản thư viện cụ thể nên xem trực tiếp trong môi trường hoặc notebook của repository khi chạy lại.

---

# 27. Hạn chế

Dự án có một số giới hạn cần được đọc cùng kết quả:

- dữ liệu tài chính có nhiều nhiễu và quan hệ thay đổi theo thời gian;
- horizon dài tạo các target tương lai chồng lấn giữa các phiên gần nhau;
- ARM kiểm tra association, không chứng minh nhân quả;
- Lift > 1 không đồng nghĩa với ý nghĩa thống kê;
- chưa thực hiện kiểm định nhiều phép thử cho hàng nghìn luật;
- chưa xây dựng chiến lược giao dịch hoặc đánh giá lợi nhuận;
- dữ liệu ngày không đảm bảo mọi thị trường đóng cửa tại cùng một thời điểm nội ngày;
- nhiều luật tốt trên Validation không giữ được trên Test.

---

# 28. Kết luận chính

Dự án cho thấy bài toán dự đoán hướng Gold là một bài toán khó và phụ thuộc rõ vào horizon.

Classification cho thấy việc bổ sung Oil, Dollar Index và S&P 500 **không tạo ra cải thiện nhất quán** so với chỉ sử dụng dữ liệu Gold.

ARM bổ sung một góc nhìn quan trọng:

> Các biến thị trường bên ngoài vẫn tạo ra nhiều mối liên hệ với Gold trong những điều kiện cụ thể, nhưng các mối liên hệ này không ổn định tuyệt đối theo thời gian và không giữ hiệu lực giống nhau ở mọi horizon.

Trong 2,289 luật được Train phát hiện và Validation chấp nhận, có 1,042 luật vẫn đạt `Lift > 1` và có tiền đề xuất hiện ít nhất 30 lần trên Test. Tuy nhiên, một lượng lớn luật khác suy giảm hoặc mất liên hệ khi sang giai đoạn Test.

Do đó kết luận của dự án không phải:

> “External markets luôn giúp dự đoán Gold.”

Mà là:

> **Quan hệ giữa Gold và các thị trường bên ngoài có tính điều kiện, phụ thuộc horizon và có thể thay đổi theo thời gian.**

---

# 29. Tài liệu nộp kèm

Repository phục vụ bài nộp cuối kỳ gồm các thành phần chính:

- notebook EDA;
- notebook Classification;
- notebook ARM theo 4 horizon;
- notebook ARM Final để chọn cấu hình và đánh giá Test;
- file kết quả và biểu đồ;
- báo cáo cuối kỳ;
- các tài liệu mô tả pipeline và kiểm chứng dữ liệu.

Báo cáo cuối kỳ: [52300088_52300138.docx](docs/52300088_52300138.docx).

---

## Ghi chú

Repository này phục vụ mục đích học tập trong môn **Khai phá dữ liệu và Khai phá tri thức**. Các kết quả mang tính thực nghiệm trên dữ liệu lịch sử và không được xem là khuyến nghị đầu tư hoặc dự báo tài chính thực tế.
