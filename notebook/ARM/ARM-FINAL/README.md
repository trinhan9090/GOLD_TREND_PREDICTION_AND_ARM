# ARM FINAL — Test và khám phá luật tách biệt

`arm_test.ipynb` chứa code trực tiếp xét 27 cấu hình chung trên kết quả Train/Val của bốn horizon, khóa luật và đánh giá Test. Chạy sau ARM-H1/H5/H10/H20. Nếu không cấu hình nào đủ 8 nhóm horizon × hướng thì dừng, không tự nới ngưỡng.

`arm_rule_discovery.ipynb` chạy sau arm_test, đọc luật đã khóa và phân tích đủ ba khía cạnh support, confidence, lift trên Train/Val/Test. Có biểu đồ độ dài itemset/luật, nhóm lift, external/Gold-only, số lần xuất hiện, overlap, ba chỉ số qua các tập và scatter support–confidence tô màu lift. Có top theo Val, top theo Test và ba bảng xếp hạng riêng theo từng chỉ số. Không đặt thêm ngưỡng Test hay mine lại từ Test.

Xếp hạng Test chỉ mô tả sau đánh giá. Kết quả nằm ở results/arm; code xử lý nằm trực tiếp trong notebook, không import từ src. Không giữ arm_final.ipynb cũ để tránh nhầm lẫn.
