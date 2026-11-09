# Challenge Dreamhack
[*Bypass SECCOMP-1*](https://dreamhack.io/wargame/challenges/361)

# Phân tích code

<img width="882" height="600" alt="image" src="https://github.com/user-attachments/assets/e3432aff-b0e9-429e-ac9a-0d3cace38d27" />

Chương trình cho phép nhập shellcode vào vùng nhớ có quyền `rwx` và chạy shellcode đó. Nhũng đồng thời cũng có hàm `sandbox` gọi *seccomp* để lọc các hàm syscall.

Kiểm tra *seccomp*:

<img width="766" height="329" alt="image" src="https://github.com/user-attachments/assets/d90f4284-e061-4e06-8d86-74647d92b125" />

Ở đây các hàm được liệt kê trên sẽ bị cấm. Còn lại các hàm khác vẫn được sử dụng. 
- Tất cả biến thể của `execve` đều bị chặn nên không thể tạo shell.
- Hàm `open` và `write` cũng bị chặn. Tuy nhiên vẫn còn các hàm và biến thể khác để mở file và in dữ liệu ra màn hình nên vẫn có thể đọc flag.

# Khai thác
<img width="1010" height="217" alt="image" src="https://github.com/user-attachments/assets/68abf30b-fd16-4970-82bc-720edf48c45d" />

Đầu tiên về vấn đề mở file thì `open` có một biến thể khác là `openat`. Khác biệt lớn nhát 
