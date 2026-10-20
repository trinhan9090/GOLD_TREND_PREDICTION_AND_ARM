# Dữ liệu

`eda_2010_2026` là snapshot cũ chỉ dùng EDA. 
`modeling` chứa raw 2005–2026, warm-up, feature, merge và target horizon. 
`arm` chứa transaction tạo từ dữ liệu modeling. Không dùng CSV EDA thay vào modeling; hai snapshot khác phạm vi và thời điểm tải.

Date và Target_Date phục vụ truy vết, không đưa vào feature. Model A 7 feature, B 11; không DFF. Nguồn gốc từng file được ghi trong `../project_manifest.json`.
