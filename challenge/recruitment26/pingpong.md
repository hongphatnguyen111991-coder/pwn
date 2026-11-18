# Phân tích code
<img width="932" height="490" alt="image" src="https://github.com/user-attachments/assets/69a815dc-018e-49f7-a3b0-7512cf9dc963" />

Trương chình gọi `rand()` để tạo số ngẫu nhiên qua seed là `time(0)`. Số giả ngẫu nhiên này sau đó đem đi chia lấy phần dư cho 2, trả về kết quả 0 hoặc 1.
Lấy kết quả cuối cùng so sánh với kí tự người dùng nhập vào 0 (l) hay 1 (r).

Sau 20 lần ghi điểm thì mở `getname`.

## Lỗ hổng và mục tiêu khai thác

<img width="645" height="254" alt="image" src="https://github.com/user-attachments/assets/572223cc-aae7-44a1-8596-26c0f5da8b03" />

Lỗ hổng *buffer overflow* cho phép ghi đè 64 BYTES vào buffer 32 BYTES. Chương trình có kiểm tra độ dài chuỗi nhập vào nhưng đơn giản chỉ cần đặt NULL BYTE sau 32 BYTES để bypass rồi ghi đè tiếp.

<img width="632" height="264" alt="image" src="https://github.com/user-attachments/assets/b057489d-2582-4a54-88f7-850a3cc1f9f2" />
<img width="482" height="185" alt="image" src="https://github.com/user-attachments/assets/78f0c257-cb62-4e46-865d-d13eeac01e47" />

Chương trình sẽ đưa chuỗi `echo \"%s\" > /tmp/pingpong_scoreboard` vào biến cmd. Và trong chương trình cũng có hàm `printff` để gọi system thực thi chuỗi trong cmd.
Lúc này nếu 
