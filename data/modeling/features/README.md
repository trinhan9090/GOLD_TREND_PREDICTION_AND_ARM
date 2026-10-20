# Feature trên lịch riêng

Bốn CSV mang tên nguồn, gồm raw OHLCV và feature đã chốt; có warm-up 2004 và NaN ban đầu theo công thức. Gold có 7 feature, Oil 1 signed price change, Dollar 1 return, S&P 2 return/drawdown. Được tạo bởi `00_prepare_data.ipynb` trước khi ghép lịch. Không phải các sample đã scale hoặc chia tập.
