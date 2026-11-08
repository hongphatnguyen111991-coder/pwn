# Lớp bảo vệ Seccomp
[*Video anh Trí - Lớp bảo vệ Seccomp*](https://www.youtube.com/watch?v=nrKNHrEouUU&list=PLEvZsp0uc3SFuVi6TtcahxqsEbV29lXAM&index=26)


*Seccomp* là một tính năng bảo mật của Linux Kernal, làm giới hạn các hàm syscall có thể gọi trong chương trình.

Khi kiểm tra *seccomp* thì sử dụng lệnh:
  
    seccomp-tools dump ./file

<img width="684" height="284" alt="Screenshot 2026-11-08 141410" src="https://github.com/user-attachments/assets/332cbcd8-3fdf-4bfd-986c-7187e1a5c059" />

Tại đây ta thấy các hàm trong syscall được phép gọi sẽ hiện thị như trên (White-list). Tất cả các lệnh gọi syscall khác sẽ mặc định bị chặn thực thi.

Để bypass *seccomp* thì có thể:

- Sử dụng các hàm chưa bị chặn để khai thác.

- Vô hiệu hóa, chuyển hướng chương trình để tránh *seccomp*

- Khai thác trước khi chương trình chạy *seccomp*

# Challenge Dreamhack
[*seccomp*](https://dreamhack.io/wargame/challenges/59)

## Phân tích code 

<img width="953" height="674" alt="image" src="https://github.com/user-attachments/assets/27930695-2db2-4900-84d1-4e081122f57e" />

Trong hàm main tạo sẵn vùng `rwx` để nhập shellcode và chạy thông qua các tùy chọn. Tuy nhiên trong đoạn code này có thêm hàm `syscall_filter` để lọc syscall. 
<br>

Kiểm tra seccomp để xem các hàm nào bị chặn thực thi:

<img width="684" height="280" alt="image" src="https://github.com/user-attachments/assets/f7daf4ca-5c4f-4351-b7e9-ea0b34f4216b" />

Vì trong Whitelist không có `execve` lẫn `open` nên chưa thể khai thác qua shellcode.
<br><br>

## Lỗ hổng khai thác:

<img width="634" height="521" alt="image" src="https://github.com/user-attachments/assets/96f31c75-531f-41c8-8bd9-7908d55af4d3" />

Trong hàm main còn có 1 tùy chọn cho phép nhập địa chỉ và ghi đè giá trị trong địa chỉ đó. Điều này cho phép chúng ta ghi đè lên bất kì địa chỉ nào có quyền `write` trong chương trình.

<img width="384" height="174" alt="image" src="https://github.com/user-attachments/assets/ffaab6f6-987a-4ef8-9b59-72c45b36ce53" />






