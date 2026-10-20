# README — Quy trình tìm và đánh giá luật kết hợp ARM theo Train → Validation → Test

## 1. Mục tiêu của phần ARM

Phần Association Rule Mining (ARM) được dùng để trả lời câu hỏi:

> **Có những tổ hợp trạng thái thị trường nào tại thời điểm hiện tại thường đi cùng với việc giá vàng tăng hoặc không tăng sau 1, 5, 10 hoặc 20 phiên hay không?**

ARM không được dùng như một mô hình dự đoán kiểu Logistic Regression, Random Forest, RNN hay LSTM. Thay vào đó, ARM tìm các **mối liên hệ dạng luật** giữa trạng thái hiện tại của Gold, Oil, Dollar Index và S&P 500 với hướng Gold trong tương lai.

Ví dụ:

```text
Gold_RSI_14 = Medium
AND Oil_Price_Change = Positive
AND SP500_Daily_Return = Negative
→ Gold_NonUp_H5
```

Có thể đọc bằng lời:

> Nếu RSI của Gold ở mức trung bình, giá dầu tăng và S&P 500 giảm tại phiên hiện tại, thì trạng thái đó có mối liên hệ với việc Gold không tăng sau 5 phiên.

Đây chỉ là **mối liên hệ thống kê**, không có nghĩa Oil hoặc S&P 500 là nguyên nhân làm Gold giảm.

---

# 2. Một số thuật ngữ được dùng trong README

Để dễ đọc, tài liệu này hạn chế dùng các thuật ngữ tiếng Anh khó hiểu.

| Thuật ngữ gốc | Cách gọi trong README | Ý nghĩa |
|---|---|---|
| Antecedent | **Tiền đề** | Nhóm điều kiện ở bên trái của luật |
| Consequent | **Hậu quả** | Kết quả ở bên phải của luật |
| Association rule | **Luật kết hợp / luật liên hệ** | Luật có dạng “tiền đề → hậu quả” |
| Candidate rule | **Luật ứng viên** | Luật được tìm thấy trên Train và có khả năng được giữ lại |
| Frequent itemset | **Tổ hợp trạng thái xuất hiện thường xuyên** | Một nhóm trạng thái xuất hiện đủ nhiều trong dữ liệu |
| Configuration | **Bộ ngưỡng / cấu hình lọc luật** | Bộ ba ngưỡng Support, Confidence, Lift |
| Stable rule | **Luật ổn định trên Validation** | Luật vẫn xuất hiện đủ nhiều và còn Lift > 1 trên Validation |
| Base rate | **Tỷ lệ nền** | Tỷ lệ Gold Up hoặc NonUp vốn có trong tập dữ liệu |
| Generalization | **Khả năng giữ hiệu lực trên dữ liệu mới** | Luật còn hoạt động khi chuyển sang Test |
| Discretization | **Rời rạc hóa / chuyển số thành trạng thái** | Chuyển các giá trị số thành Low/Medium/High, Positive/Negative... |
| Coverage | **Tỷ lệ xuất hiện tiền đề** | Tỷ lệ phiên có tiền đề của luật |

---

# 3. Dữ liệu đầu vào của ARM

ARM sử dụng cùng **11 đặc trưng** của Model B trong bài toán Classification:

### Nhóm Gold

1. Gold Daily Return
2. Gold Return Lag 1
3. Gold Intraday Range
4. Gold Volatility 20
5. Gold Distance to MA20
6. Gold RSI14
7. Gold MACD Histogram

### Nhóm thị trường bên ngoài

8. Oil Price Change
9. Dollar Daily Return
10. S&P 500 Daily Return
11. S&P 500 Drawdown

ARM được chạy riêng cho bốn khoảng dự báo:

- H1: hướng Gold sau 1 phiên
- H5: hướng Gold sau 5 phiên
- H10: hướng Gold sau 10 phiên
- H20: hướng Gold sau 20 phiên

Hậu quả của luật chỉ được phép là một trong hai nhãn:

```text
Gold_Up_H*
Gold_NonUp_H*
```

Trong đó `*` là 1, 5, 10 hoặc 20.

---

# 4. Vì sao phải chuyển dữ liệu số thành trạng thái?

Apriori không làm việc trực tiếp theo cách tự nhiên với những con số liên tục như:

```text
RSI = 47.3
Dollar Return = -0.0021
Volatility = 0.013
```

Do đó dữ liệu được chuyển thành các trạng thái dễ khai phá hơn.

Ví dụ:

```text
Dollar_Daily_Return = Negative
Gold_RSI_14 = Medium
Gold_Volatility_20 = High
SP500_Drawdown = Shallow
```

Các biến có dấu được chia thành:

```text
Negative / Zero / Positive
```

Các biến thể hiện mức độ được chia thành:

```text
Low / Medium / High
```

Riêng S&P 500 Drawdown dùng:

```text
Deep / Medium / Shallow
```

Ngưỡng Low/Medium/High được học **chỉ từ Train của từng horizon**, sau đó giữ nguyên khi áp dụng sang Validation và Test. Việc này tránh để thông tin từ tương lai ảnh hưởng ngược về quá trình tạo luật.

---

# 5. Mỗi phiên trở thành một “giao dịch trạng thái”

Sau khi rời rạc hóa, mỗi phiên được xem như một tập các trạng thái cùng xuất hiện.

Ví dụ một phiên H5 có thể trở thành:

```text
Gold_RSI_14=Medium
Gold_Volatility_20=High
Gold_MACD_Histogram=Negative
Oil_Price_Change=Positive
Dollar_Daily_Return=Negative
SP500_Daily_Return=Positive
SP500_Drawdown=Shallow
Gold_Up_H5
```

Apriori sẽ tìm xem những trạng thái nào thường xuất hiện cùng nhau.

---

# 6. Bước Train — Apriori tìm luật như thế nào?

## 6.1. Apriori chưa tìm luật ngay

Đầu tiên Apriori tìm các **tổ hợp trạng thái xuất hiện thường xuyên**.

Ví dụ:

```text
{Dollar=Negative}
```

sau đó:

```text
{Dollar=Negative, Gold_RSI=Low}
```

sau đó:

```text
{Dollar=Negative, Gold_RSI=Low, Gold_Up_H5}
```

Trong bài này:

```text
min_support để khai phá = 0.02
số item tối đa trong một tổ hợp = 4
```

`Support >= 0.02` nghĩa là tổ hợp phải xuất hiện trong ít nhất khoảng 2% số phiên Train.

Apriori dùng quy tắc:

> Nếu một tổ hợp nhỏ đã xuất hiện quá ít, thì mọi tổ hợp lớn hơn chứa nó cũng chắc chắn không thể xuất hiện nhiều hơn.

Nhờ vậy thuật toán có thể bỏ sớm rất nhiều tổ hợp không cần kiểm tra.

---

## 6.2. Vì sao mine ở Support = 0.02?

Bộ ngưỡng được thử sau đó có:

```text
Support ∈ {0.02, 0.05, 0.10}
```

Do `0.02` là mức thấp nhất nên chỉ cần khai phá một **tập luật ứng viên đủ rộng** ở mức Support 0.02.

Nếu một luật có:

```text
Support Train < 0.02
```

thì nó chắc chắn không thể đạt các mức:

```text
0.02, 0.05 hoặc 0.10
```

Do đó không cần chạy lại Apriori 27 lần từ đầu.

---

# 7. Từ tổ hợp trạng thái sang luật

Sau khi tìm được tổ hợp trạng thái đủ phổ biến, chương trình tạo luật có dạng:

```text
Tiền đề → Hậu quả
```

Ví dụ:

```text
Dollar_Daily_Return=Negative
AND Gold_RSI_14=Low
→ Gold_Up_H5
```

Trong bài:

- Tiền đề có từ **1 đến 3 trạng thái**
- Hậu quả có đúng **1 nhãn Gold**
- Hậu quả không được xuất hiện trong tiền đề
- Luật có thể gồm:
  - 1 tiền đề + 1 hậu quả
  - 2 tiền đề + 1 hậu quả
  - 3 tiền đề + 1 hậu quả

Do đó `max itemset size = 4` là **giới hạn trên**, không có nghĩa mọi luật đều bắt buộc phải có 3 điều kiện.

---

# 8. Ba chỉ số chính của một luật

Giả sử:

```text
A → Gold_Up_H5
```

## 8.1. Support — độ phổ biến của toàn bộ luật

Support đo tỷ lệ phiên vừa có tiền đề `A`, vừa có hậu quả `Gold_Up_H5`.

```text
Support = số lần (A và Gold_Up_H5 cùng xảy ra) / tổng số phiên
```

Ví dụ:

- 1000 phiên
- A và Gold Up cùng xuất hiện 60 lần

thì:

```text
Support = 60 / 1000 = 0.06
```

---

## 8.2. Confidence — xác suất hậu quả khi tiền đề xảy ra

Confidence trả lời:

> Khi tiền đề xuất hiện, hậu quả xảy ra bao nhiêu phần trăm?

```text
Confidence = số lần tiền đề + hậu quả cùng xảy ra
             / số lần tiền đề xuất hiện
```

Ví dụ:

- tiền đề A xuất hiện 80 lần
- trong đó 60 lần Gold Up

thì:

```text
Confidence = 60 / 80 = 0.75
```

---

## 8.3. Lift — mức mạnh hơn so với tỷ lệ nền

Lift trả lời:

> Khi tiền đề xảy ra, hậu quả có xuất hiện nhiều hơn mức bình thường không?

```text
Lift = Confidence / Tỷ lệ nền của hậu quả
```

Nếu:

```text
Confidence = 0.75
Tỷ lệ Gold Up bình thường = 0.60
```

thì:

```text
Lift = 0.75 / 0.60 = 1.25
```

Diễn giải:

> Trong những phiên có tiền đề này, Gold Up xuất hiện nhiều hơn khoảng 25% tương đối so với mức nền.

Cách đọc:

- `Lift > 1`: có liên hệ dương
- `Lift = 1`: gần mức nền
- `Lift < 1`: hậu quả xuất hiện ít hơn mức nền

Lift cao **không đồng nghĩa** Confidence cao. Hai chỉ số trả lời hai câu hỏi khác nhau.

---

# 9. Train tạo ra tập luật ứng viên

Sau bước Apriori và tạo luật, mỗi horizon có một tập luật ứng viên.

Kết quả thực tế:

| Horizon | Luật ứng viên trên Train |
|---|---:|
| H1 | 4,374 |
| H5 | 4,341 |
| H10 | 4,328 |
| H20 | 4,335 |

Các luật này chưa phải kết quả cuối cùng.

Train chỉ trả lời:

> “Những luật nào có khả năng đáng xem xét?”

---

# 10. 27 bộ ngưỡng được tạo như thế nào?

Nhóm định nghĩa trước ba mức Support, ba mức Confidence và ba mức Lift:

```text
Support    = {0.02, 0.05, 0.10}
Confidence = {0.50, 0.55, 0.60}
Lift       = {1.00, 1.05, 1.10}
```

Số tổ hợp là:

```text
3 × 3 × 3 = 27 bộ ngưỡng
```

Ví dụ:

```text
Bộ A = Support ≥ 0.02, Confidence ≥ 0.50, Lift ≥ 1.00
Bộ B = Support ≥ 0.05, Confidence ≥ 0.55, Lift ≥ 1.05
Bộ C = Support ≥ 0.10, Confidence ≥ 0.60, Lift ≥ 1.10
```

### Quan trọng

27 bộ ngưỡng này:

- **không được Apriori tự học**
- **không sinh ngẫu nhiên**
- **không được Test quyết định**

Đây là **lưới ngưỡng do nhóm định nghĩa trước** để so sánh nhiều mức lọc khác nhau.

Có thể hình dung 27 bộ ngưỡng như **27 cái rây** có độ chặt khác nhau cùng lọc một tập luật ứng viên.

Một luật có thể thuộc nhiều bộ ngưỡng cùng lúc.

Ví dụ:

```text
Support Train    = 0.07
Confidence Train = 0.57
Lift Train       = 1.08
```

Luật này sẽ vượt qua các bộ ngưỡng tương đối lỏng, nhưng không vượt qua bộ yêu cầu:

```text
Support ≥ 0.10
hoặc Confidence ≥ 0.60
hoặc Lift ≥ 1.10
```

---

# 11. Validation — chọn bộ ngưỡng tốt nhất

Validation không chạy Apriori lại để tìm luật mới.

Thay vào đó:

1. Lấy các luật đã được tìm trên Train
2. Áp từng bộ trong 27 bộ ngưỡng
3. Đem các luật còn lại sang Validation
4. Đếm lại số lần xuất hiện và tính lại Support, Confidence, Lift trên Validation

Một luật được xem là **ổn định trên Validation** khi:

```text
Số lần tiền đề xuất hiện trên Validation ≥ 30
AND
Lift Validation > 1
```

Ngưỡng 30 lần giúp tránh việc một luật chỉ xuất hiện vài lần nhưng có Confidence hoặc Lift rất cao do ngẫu nhiên.

---

# 12. Vì sao có 8 nhóm khi chọn cấu hình?

Có:

```text
4 horizon × 2 hướng = 8 nhóm
```

Cụ thể:

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

Một bộ ngưỡng chỉ được phép cạnh tranh nếu **cả 8 nhóm đều có ít nhất một luật ổn định trên Validation**.

Nếu một bộ ngưỡng quá chặt khiến một nhóm không còn luật nào thì bộ đó bị loại.

---

# 13. Score của một bộ ngưỡng được tính như thế nào?

Trong mỗi nhóm, lấy tất cả các luật ổn định và tính:

```text
Median Lift Validation
```

Ví dụ một bộ ngưỡng có:

```text
H1-Up      → median lift = 1.07
H1-NonUp   → median lift = 1.08
H5-Up      → median lift = 1.06
H5-NonUp   → median lift = 1.09
H10-Up     → median lift = 1.08
H10-NonUp  → median lift = 1.10
H20-Up     → median lift = 1.09
H20-NonUp  → median lift = 1.13
```

Sau đó lấy **trung bình của 8 giá trị median này**:

```text
Score = Mean(8 group median lifts)
```

Vì vậy:

> Median được dùng **bên trong từng nhóm**, sau đó Mean được dùng để tổng hợp 8 nhóm thành một Score cho mỗi bộ ngưỡng.

Cuối cùng chọn bộ ngưỡng có Score cao nhất.

Nếu hòa, ưu tiên tập luật có độ dài tiền đề trung bình ngắn hơn; nếu vẫn hòa thì ưu tiên bộ ngưỡng chặt hơn.

---

# 14. Bộ ngưỡng thắng

Validation đã chọn:

```text
min_support    = 0.02
min_confidence = 0.50
min_lift       = 1.00
```

Score Validation:

```text
1.087585
```

Điều này không có nghĩa các mức 0.02 / 0.50 / 1.00 là “chân lý”.

Nó chỉ có nghĩa:

> Trong 27 bộ ngưỡng đã định nghĩa trước, bộ này tạo ra tập luật ổn định trên Validation tốt nhất theo tiêu chí cân bằng 8 nhóm mà nhóm đã đặt ra.

---

# 15. Các luật được chốt sau Validation

Sau khi chọn bộ ngưỡng thắng, giữ các luật:

1. thuộc bộ ngưỡng thắng trên Train;
2. và ổn định trên Validation.

Số luật được chốt:

| Horizon | Luật ứng viên Train | Luật được chốt sau Validation |
|---|---:|---:|
| H1 | 4,374 | 835 |
| H5 | 4,341 | 476 |
| H10 | 4,328 | 442 |
| H20 | 4,335 | 536 |
| **Tổng** | — | **2,289** |

Phân bố theo hướng:

| Horizon | Up | NonUp |
|---|---:|---:|
| H1 | 548 | 287 |
| H5 | 428 | 48 |
| H10 | 400 | 42 |
| H20 | 453 | 83 |

Sau bước này, danh sách luật được **khóa**.

Điều đó có nghĩa là:

- không đổi cấu hình sau khi nhìn Test;
- không thêm luật vì Test đẹp;
- không xóa luật vì Test xấu.

---

# 16. Test — kiểm tra khả năng giữ hiệu lực trên dữ liệu mới

Toàn bộ **2,289 luật đã chốt** được đưa sang Test.

Test không tìm thêm luật mới.

Với từng luật, chương trình chỉ:

1. đếm số lần tiền đề xuất hiện;
2. đếm số lần tiền đề và hậu quả cùng xuất hiện;
3. tính lại Support;
4. tính lại Confidence;
5. tính lại Lift.

Mục tiêu là trả lời:

> Những mối liên hệ được tìm trên Train và được Validation chấp nhận có còn giữ được trên giai đoạn dữ liệu mới hay không?

---

# 17. Cách chia kết quả Test

Để mô tả kết quả, luật được chia thành bốn nhóm:

### Nhóm 1 — còn liên hệ và xuất hiện đủ nhiều

```text
Lift Test > 1
AND
Số lần tiền đề xuất hiện trên Test ≥ 30
```

### Nhóm 2 — còn Lift > 1 nhưng xuất hiện ít

```text
Lift Test > 1
AND
Số lần tiền đề < 30
```

### Nhóm 3 — không còn liên hệ dương

```text
Lift Test ≤ 1
```

### Nhóm 4 — không đủ dữ liệu để tính Lift

Ví dụ tiền đề không xuất hiện trong Test.

### Lưu ý

Ngưỡng `30 lần` và `Lift > 1` là quy ước mô tả độ bền của luật, **không phải kiểm định ý nghĩa thống kê**.

---

# 18. Kết quả Test tổng thể

Trong 2,289 luật đã chốt:

| Kết quả Test | Số luật | Tỷ lệ |
|---|---:|---:|
| Lift > 1 và tiền đề xuất hiện ≥ 30 lần | **1,042** | **45.5%** |
| Lift > 1 nhưng tiền đề xuất hiện < 30 lần | 238 | 10.4% |
| Lift ≤ 1 | 990 | 43.3% |
| Không tính được Lift | 19 | 0.8% |
| **Tổng** | **2,289** | **100%** |

Có thể diễn giải:

> Gần một nửa số luật được Train phát hiện và Validation chấp nhận vẫn giữ được Lift > 1 với số lần xuất hiện đủ lớn trên Test.

Tuy nhiên không nên nói rằng 1,042 luật này “đã được chứng minh đúng”. Chúng chỉ cho thấy **mối liên hệ vẫn còn xuất hiện trên dữ liệu Test theo tiêu chí mô tả của bài**.

---

# 19. Kết quả theo từng horizon

| Horizon | Luật chốt | Test: Lift > 1 và ≥30 lần | Lift > 1 nhưng <30 | Lift ≤1 | Không tính được |
|---|---:|---:|---:|---:|---:|
| H1 | 835 | 449 | 70 | 311 | 5 |
| H5 | 476 | 261 | 49 | 166 | 0 |
| H10 | 442 | 181 | 55 | 197 | 9 |
| H20 | 536 | 151 | 64 | 316 | 5 |

Median toàn bộ luật theo horizon:

| Horizon | Median Support Test | Median Confidence Test | Median Lift Test |
|---|---:|---:|---:|
| H1 | 0.0542 | 0.5466 | 1.0322 |
| H5 | 0.0586 | 0.6387 | 1.0450 |
| H10 | 0.0534 | 0.6129 | 1.0115 |
| H20 | 0.0469 | 0.6267 | 0.9570 |

H5 có median Lift Test cao nhất trong bốn horizon, trong khi H20 có median Lift dưới 1.

---

# 20. Up và NonUp có hành vi khác nhau

Nếu xem riêng median Lift Test theo hướng:

| Horizon | Up — Median Lift Test | NonUp — Median Lift Test |
|---|---:|---:|
| H1 | 1.0277 | 1.0383 |
| H5 | 1.0517 | 0.9535 |
| H10 | 1.0195 | 0.9206 |
| H20 | 0.9592 | 0.9481 |

Điều đáng chú ý:

- H1: cả Up và NonUp vẫn quanh hoặc trên 1.
- H5: luật Up giữ được khá tốt, trong khi NonUp giảm xuống dưới 1.
- H10: Up vẫn nhỉnh hơn 1, NonUp giảm rõ.
- H20: cả hai hướng đều có median Lift dưới 1.

Do đó có thể nói:

> **Các luật hướng tới Gold Up nhìn chung giữ mối liên hệ tốt hơn các luật NonUp ở H5 và H10. Tuy nhiên đến H20, cả hai hướng đều suy giảm.**

Không nên nói “mọi luật Up đều tồn tại”, vì trong từng nhóm vẫn có nhiều luật Test Lift ≤ 1. Nhận xét trên là nhận xét về **xu hướng tổng thể / trung vị**.

---

# 21. Ví dụ một luật giữ được tốt trên Test

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
Test Confidence = 31 / 64 ≈ 0.484
Test Lift ≈ 1.268
```

Mặc dù Confidence Test chỉ khoảng 48.4%, Lift vẫn lớn hơn 1 vì tỷ lệ nền của NonUp H5 thấp hơn mức 48.4%.

Đây là ví dụ cho thấy:

> Confidence không nên được đọc một mình; cần so với tỷ lệ nền thông qua Lift.

---

# 22. Ví dụ một luật đẹp trên Validation nhưng không giữ được trên Test

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

Luật này rất mạnh trên Validation nhưng sang Test thì Lift xuống dưới 1.

Đây là ví dụ điển hình của việc:

> Một luật có thể phù hợp với một giai đoạn thị trường nhưng không giữ được khi điều kiện thị trường thay đổi.

---

# 23. Ý nghĩa của biểu đồ Support — Confidence — Lift trên Test

Trong biểu đồ scatter của 2,289 luật:

- Trục X: Support Test
- Trục Y: Confidence Test
- Màu: Lift Test
- Mỗi điểm: một luật đã chốt

Biểu đồ không dùng để chọn lại luật.

Nó chỉ được dùng **sau khi Test đã hoàn tất** để quan sát:

- luật nào phổ biến;
- luật nào có Confidence cao;
- luật nào có Lift cao;
- các chỉ số này có luôn đi cùng nhau hay không.

Một luật có Confidence cao chưa chắc Lift cao nếu hậu quả vốn đã có tỷ lệ nền cao.

Một luật có Lift rất cao cũng chưa chắc đáng tin nếu tiền đề chỉ xuất hiện vài lần.

---

# 24. Vai trò của Train, Validation và Test — cách nhớ ngắn nhất

```text
TRAIN
  ↓
Rời rạc hóa dữ liệu bằng ngưỡng học từ Train
  ↓
Apriori tìm các tổ hợp trạng thái thường xuyên
  ↓
Sinh tập luật ứng viên
  ↓
27 bộ ngưỡng lọc cùng tập luật ứng viên
  ↓
VALIDATION
  ↓
Đánh giá lại từng bộ ngưỡng
  ↓
Chỉ giữ luật có tiền đề ≥30 lần và Lift >1
  ↓
Tính median Lift cho 8 nhóm
  ↓
Lấy mean của 8 median → Score của cấu hình
  ↓
Chọn cấu hình có Score cao nhất
  ↓
Khóa các luật của cấu hình thắng
  ↓
TEST
  ↓
Không tìm luật mới
  ↓
Tính lại Support / Confidence / Lift
  ↓
Đánh giá khả năng giữ hiệu lực trên dữ liệu mới
```

Có thể nhớ bằng bốn từ:

```text
Train       = TÌM
Validation  = CHỌN
Lock        = CHỐT
Test        = KIỂM TRA
```

---

# 25. Mối liên hệ giữa ARM và bài toán Classification

Classification trả lời:

> Dùng các đặc trưng hiện tại có dự đoán được Gold Up/NonUp hay không?

ARM trả lời:

> Có những tổ hợp trạng thái cụ thể nào liên hệ với Gold Up/NonUp hay không?

Model B thêm Oil, Dollar và S&P 500 nhưng không phải lúc nào cũng tốt hơn Model A.

Kết quả ARM giúp giải thích rằng:

> Thông tin từ các thị trường bên ngoài không hoàn toàn vô ích, nhưng mối liên hệ của chúng với Gold có tính **phụ thuộc điều kiện và phụ thuộc horizon**.

Một số tổ hợp giữ được trên Test, trong khi nhiều tổ hợp khác chỉ mạnh trên Validation rồi suy giảm.

Vì vậy không nên kết luận:

```text
External features luôn giúp dự đoán Gold.
```

Cách kết luận phù hợp hơn là:

> **Các biến thị trường bên ngoài có thể mang thông tin hữu ích trong một số trạng thái cụ thể, nhưng các mối liên hệ này không ổn định tuyệt đối giữa các giai đoạn và các horizon.**

---

# 26. Những điều không nên kết luận từ ARM

Không nên viết:

> “Oil tăng gây ra Gold giảm.”

ARM chỉ tìm mối liên hệ, không chứng minh nguyên nhân.

Không nên viết:

> “Lift > 1 nghĩa là luật có ý nghĩa thống kê.”

Lift không phải kiểm định ý nghĩa thống kê.

Không nên viết:

> “1,042 luật đã được chứng minh đúng.”

Đúng hơn là:

> “1,042 luật vẫn có Lift > 1 và tiền đề xuất hiện ít nhất 30 lần trên Test.”

Không nên chọn lại các luật đẹp nhất bằng Test rồi gọi chúng là luật đã được chọn từ trước.

Các bảng xếp hạng Test chỉ là **phân tích sau đánh giá**, không phải bước lựa chọn mới.

---

# 27. Tóm tắt toàn bộ quy trình bằng lời

Quy trình bắt đầu bằng việc chuyển các đặc trưng số thành các trạng thái dễ hiểu như Positive, Negative, Low, Medium và High. Apriori sử dụng dữ liệu Train để tìm những tổ hợp trạng thái xuất hiện đủ thường xuyên và từ đó tạo ra các luật ứng viên có dạng **tiền đề → hậu quả**, trong đó hậu quả luôn là Gold Up hoặc Gold NonUp ở một horizon xác định.

Thay vì chọn trực tiếp một ngưỡng Support, Confidence và Lift theo cảm tính, nhóm định nghĩa trước 27 bộ ngưỡng. Đây là 27 cách lọc khác nhau trên cùng tập luật ứng viên. Validation được dùng để kiểm tra các luật của từng bộ ngưỡng trên một giai đoạn thời gian chưa dùng để khai phá luật. Một luật chỉ được xem là ổn định nếu tiền đề xuất hiện ít nhất 30 lần và Lift Validation lớn hơn 1.

Mỗi bộ ngưỡng được đánh giá cân bằng trên 8 nhóm gồm 4 horizon × 2 hướng. Trong từng nhóm lấy median Lift Validation, sau đó lấy trung bình của 8 median để tạo thành Score của bộ ngưỡng. Bộ ngưỡng có Score cao nhất được chọn. Trong thực nghiệm, bộ thắng là Support 0.02, Confidence 0.50 và Lift 1.00.

Các luật thuộc bộ ngưỡng thắng và đạt điều kiện Validation được khóa lại. Tổng cộng có 2,289 luật. Toàn bộ số luật này sau đó được đưa sang Test mà không thay đổi. Test không tạo thêm luật và cũng không loại luật xấu. Nó chỉ tính lại Support, Confidence và Lift để kiểm tra xem các mối liên hệ đã phát hiện trước đó có còn tồn tại trên dữ liệu mới hay không.

Kết quả cho thấy 1,042/2,289 luật, tương đương 45.5%, vẫn có Lift > 1 và tiền đề xuất hiện ít nhất 30 lần trên Test. Các luật hướng tới Gold Up nhìn chung giữ được tốt hơn tại H5 và H10, trong khi nhiều luật NonUp suy giảm khi chuyển sang Test. Đến H20, median Lift của cả Up và NonUp đều dưới 1. Điều này cho thấy mối liên hệ giữa Gold và các trạng thái thị trường có tồn tại, nhưng phụ thuộc vào horizon và không ổn định hoàn toàn theo thời gian.

---

# 28. Nguồn đã đối chiếu khi viết README này

README này được tổng hợp và đối chiếu với:

- `arm_test.ipynb`: chọn 1 cấu hình chung trên Validation, khóa luật và đánh giá Test.
- `arm_rule_discovery.ipynb`: phân tích Support, Confidence, Lift sau khi đánh giá Test.
- `H1_rules.csv`, `H5_rules.csv`, `H10_rules.csv`, `H20_rules.csv`: tập luật ứng viên Train/Validation.
- `H1_selected_rules.csv`, `H5_selected_rules.csv`, `H10_selected_rules.csv`, `H20_selected_rules.csv`: luật được chốt sau Validation.
- `H1_evaluated_rules.csv`, `H5_evaluated_rules.csv`, `H10_evaluated_rules.csv`, `H20_evaluated_rules.csv`: luật được đánh giá trên Test.
- `summary.csv`: thống kê tổng hợp theo horizon.

Các số liệu trong README được lấy từ các file kết quả được cung cấp, không tự suy đoán lại kết quả thực nghiệm.
