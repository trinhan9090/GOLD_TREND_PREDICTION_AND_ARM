# Nguồn và chất lượng dữ liệu tải

`*_snapshot_response.json` và `*_warmup_response.json` giữ phản hồi Yahoo gốc cho 4 nguồn; `gold_horizon_support_response.json` cho nhãn cuối. `*_unavailable_quotes.csv` ghi các quote Close thiếu đã không được coi là phiên quan sát; file rỗng có header nghĩa là không có quote bị loại, vẫn giữ để truy vết.

`download_manifest.json` là nhật ký tải gốc, có thể nhắc bản snapshot chuẩn trung gian hoặc gold_next_sessions không được sao chép vì trùng dữ liệu. `gold_horizon_manifest.json` mô tả hỗ trợ target mới nhất. Các URL, timezone và retrieved_utc là lịch sử tải, không phải yêu cầu tự crawl lại. Dữ liệu thực dùng nằm ở `../raw` và `../support`.
