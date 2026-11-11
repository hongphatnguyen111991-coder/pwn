# Egg hunter
[*video anh Trí - Egg hunter*](https://youtu.be/hun5c_WdquY)

*Egg hunter* là kĩ thuật sử dụng để tìm shellcode hay dữ liệu thông qua kiểm tra signature, các dấu hiệu đặc trưng của đối tượng đó. *Egg hunter* được dùng khi chương trình chỉ cho phép chạy 1 đoạn shellcode rất nhỏ. Vì không đủ kích thước tạo shell hay mở flag, người ta dùng nó để tìm shellcode lớn hơn hay flag được lưu trữ trong chương trình.

# Challenge

<img width="673" height="389" alt="image" src="https://github.com/user-attachments/assets/09500ec2-b86c-4a04-a134-a1b5ebc3ae58" />

Chương trình cho phép nhập shellcode và thực thi. 

Đồng thời cũng có *seccomp* chặn một số hàm quan trọng:

<img width="845" height="425" alt="image" src="https://github.com/user-attachments/assets/3a44f0a5-c519-4d32-9369-6e10e3237cdf" />
