# Race condition
[*Video anh Trí - Race condition*](https://www.youtube.com/watch?v=iwQUv6ShtEM&list=PLEvZsp0uc3SFuVi6TtcahxqsEbV29lXAM&index=30)

Race condition xảy ra khi có ít nhất 2 luồng (threads) đang chạy và cùng truy cập các biến dùng chung tại cùng 1 thời điểm. Nếu đồng bộ hóa không tốt thì
có thể làm kết quả sai lệch và tạo ra lỗ hổng bảo mật.

# Challenge

<img width="966" height="730" alt="image" src="https://github.com/user-attachments/assets/a6a2977d-c5d6-4e63-bc8a-c4f824991f42" />

Trong chương trình này có 2 option: 

- Một là mở hàm thay đổi biến `is_admin` thành 1 và sau khoảng thời gian ngắn trả `is_admin` về 0.
- Hai là thử điều kiện nếu `is_admin` khác 0 thì tạo shell.

Lỗ hổng ở đây là luồng con sau khi chỉnh `is_admin` thành 1 thì `usleep(250000)` làm cho luồng ngưng lại . Trong khi đó, luồng cha vẫn có thể thực thi tiếp câu lệnh
tiếp theo và chọn option 2. Kết quả là trong thoáng chốc người dùng có quyền gọi shell trước khi `is_admin` được trả về 0 khi hết sleep.

<img width="1273" height="854" alt="image" src="https://github.com/user-attachments/assets/137d3f82-50af-4244-bf36-8c01b633823a" />

Như tại câu lệnh `usleep` này thì cả 2 thread đều truy cập `is_admin` và thấy giá trị của biến này bằng 1. Lúc này chỉ cần tại thread 1 chạy option 2
kiểm tra điều kiện thì sẽ tọa được shell.
