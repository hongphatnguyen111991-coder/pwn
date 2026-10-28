# Link Challenge Dreamhack

[Return to Library](https://dreamhack.io/wargame/challenges/353)

# Phân tích code 

<img width="831" height="640" alt="image" src="https://github.com/user-attachments/assets/3a89e63a-8d3b-407d-b837-4f11ccdb791a" />
<img width="766" height="206" alt="image" src="https://github.com/user-attachments/assets/a23e72e2-449d-4b60-99d2-4210b94a700a" />

Chương trình đưa sẵn system vào bảng PLT tức ta có thể gọi `exe.sym['system']` để lấy địa chỉ hàm system. Đồng thời chương trình cũng tạo sẵn
biến chứa chuỗi `/bin/sh` chỉ cần tìm địa chỉ rồi đưa vào làm tham số thứ nhất khi gọi system.

Mitigation:

Đồng thời *PIE* cũng tắt nên không cần leak 
binary address. Tuy nhiên vẫn có *Canary* nên cần leak *Canary* trước.

# *Lưu ý*

<img width="1401" height="965" alt="Screenshot 2026-10-28 181947" src="https://github.com/user-attachments/assets/a7ca135e-e134-4108-980c-6173834b1a5c" />

Khi DEBUG thì chạy đến hàm system bị ngắt luồng thực thi. Vì khi gọi system thì tiến trình Inferior 1 (cha) đã tạo 1 tiến trình Inferior (con).
Tiến trình con này sau khi in ra màn hình `'system@plt'` thì kết thúc.

Để quay lại tiến trình cha thì dùng lệnh `attach pid` của tiến trình Inferior 1:

<img width="902" height="195" alt="image" src="https://github.com/user-attachments/assets/f0d2e151-455b-4c6b-8acc-f2e1c26bea10" />

# 




