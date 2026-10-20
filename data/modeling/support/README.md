# Dữ liệu hỗ trợ, không phải mẫu nghiên cứu

`gold_warmup.csv`, `oil_warmup.csv`, `dollar_index_warmup.csv`, `sp500_warmup.csv`: lịch sử 2004 để khởi tạo rolling/RSI/MACD/drawdown. `gold_horizon_support.csv`: 20 phiên 21/09–16/10/2026, chỉ tạo target cuối cho H1/H5/H10/H20. H1 lấy phiên đầu sau snapshot từ chính file này, không giữ bản gold_next_sessions trùng mục đích.

Các bảng có Date và OHLCV chuẩn, nguồn Yahoo; provenance ở thư mục bên cạnh. Không dùng giá hỗ trợ tương lai làm feature tại t.
