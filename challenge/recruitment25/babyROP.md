# Phân tích code
<img width="852" height="331" alt="image" src="https://github.com/user-attachments/assets/9726f692-dd21-4a0d-ab11-ec1ff253cd85" />

Trong chương trình này có lỗ hổng *buffer overflow*. Bên dưới có kiểm duyệt độ dài chuỗi nhưng có thể bypass bằng cách nhập NULL BYTE giữa payload.

## Mitigation
<img width="808" height="277" alt="image" src="https://github.com/user-attachments/assets/259b0241-6c6b-4011-8942-4f79c46c20fc" />

No PIE nên các địa chỉ binary cố định để khai thác.

## Gadget
<img width="1167" height="143" alt="image" src="https://github.com/user-attachments/assets/c47602cf-ead5-4aae-b8b9-d18fcd082d1f" />

Các gadget trên không đủ để ta xây dựng ROPchain syscall execve. Chỉ có khả năng điều khiển thanh ghi rax.

## Leak libc
<img width="656" height="422" alt="image" src="https://github.com/user-attachments/assets/07861a98-2bde-4c5d-86aa-2b2c2d5bbd32" />

Quay lại mã được dịch ngược ở dạng Assembly thì thấy `mov rdi, rax`. Và dùng `puts` in dữ liệu trong rdi ra màn hình.
Mà nhờ có gadget kiểm soát rax và No PIE mà ta có thể in địa chỉ libc trong binary.

Payload:

<img width="1595" height="916" alt="image" src="https://github.com/user-attachments/assets/09c98122-d2a8-4ea8-8238-ddc6e8bd1d19" />

- NULL BYTES : bypass kiểm duyệt độ dài chuỗi
- saved rbp -> rw_section : Vì tí nữa sẽ dính *Stack pivot* nên cần đưa vào địa chỉ hợp lệ.
- saved rip -> pop_rax : Lấy địa chỉ GOT chứa hàm libc đẩy vào rax
- exe.got['puts']
- exe.sym['main']+29 : Quay về main để gọi `puts` leak libc

