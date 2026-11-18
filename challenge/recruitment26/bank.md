# Phân tích code
<img width="1027" height="675" alt="image" src="https://github.com/user-attachments/assets/8176515d-ddaf-4d80-8889-a41a26c7f63b" />

Sau khi đã đăng kí tài khoản thì chương trình cho 4 lựa chọn để tiếp tục. 

Tạo script login sẵn:

    #!/usr/bin/env python3
    from pwn import *
    exe = ELF("./bank_patched")
    libc = ELF("./libc.so.6")
    ld = ELF("./ld-2.35.so")
    context.binary = exe
    p=process('bank_patched')
    
    p.sendlineafter(b'Choice:',b'1')      //tạo tài khoản
    p.sendlineafter(b'Username:',b'zyan')
    p.sendlineafter(b'Password:',b'1')
    p.sendlineafter(b'Description:',b'Description')
    
    p.sendlineafter(b'Choice:',b'2')      //login
    p.sendlineafter(b'Username:',b'zyan')
    p.sendlineafter(b'Password:',b'1')
## Lỗ hổng và mục tiêu khai thác
<img width="482" height="272" alt="image" src="https://github.com/user-attachments/assets/cd0e6839-444e-455b-9831-7e87fc7e749c" />
<img width="970" height="660" alt="image" src="https://github.com/user-attachments/assets/e03f83c1-65f7-4ca5-94e3-7afa6bd32db7" />

Tại hàm `changeDescription` có 1 lỗ hổng *buffer overflow*. Do Description vốn chỉ có kích thước 0x10 BYTES, mà chương trình lại cho phép nhập tới 0x20 BYTES.
Bên cạnh đó, ta còn thấy chương trình mở sẵn flag ở hàm `win`. 

<img width="797" height="173" alt="image" src="https://github.com/user-attachments/assets/187a5558-d307-44ea-bf44-14a93f84a569" />

Vùng nhớ được khoanh vùng là 0x10 BYTES của Description. VÌ có thể ghi đè đến 0x20 BYTES nên có thể ghi đè lên hàm `viewBalance`.

## Mitigation
<img width="800" height="282" alt="image" src="https://github.com/user-attachments/assets/8eec8a5e-0281-40f3-a5b5-b70b2d7e7c66" />

Vì PIE bật nên muốn ghi đè hàm `win` lên `viewBalance` thì đầu tiên cần có binary base.

## Leak binary

<img width="610" height="134" alt="image" src="https://github.com/user-attachments/assets/def2f8c6-0b9b-4866-84eb-83c89f4327a0" />
<img width="446" height="95" alt="image" src="https://github.com/user-attachments/assets/2bd9d312-1f07-4d1b-a19b-d762c21e5441" />

Ý tưởng ban đầu là tận dụng luôn `changeDescription` để nối chuỗi leak hàm `viewBalance`. Tuy nhiên ở hàm `changeDescription` có một lệnh ghi đè NULL BYTE vào cuối chuỗi khiên cho việc leak theo cách này bất khả thi.

Tuy nhiên nếu phân tích kĩ code thì ta sẽ thấy có 1 hàm gián tiếp giúp ta nối chuỗi thành công.

<img width="567" height="187" alt="image" src="https://github.com/user-attachments/assets/3cfb85ad-bc22-42ec-b35d-53ac2a2706cc" />
<img width="790" height="210" alt="image" src="https://github.com/user-attachments/assets/04b90a50-6c50-4ae2-b42e-27b63c81d70f" />

Ở dưới Description còn có 1 ô nhớ 8 BYTES. Đây chính là `state.balance`. Mỗi khi ta đưa feed back lên thì chương trình sẽ cộng thêm 1 vào `state.balence`. Và nếu như ta cộng đủ nhiều thì ô nhớ đó sẽ không còn NULL BYTE nào làm cho việc nỗi chuỗi là khả thi.

chuỗi không có `NULL BYTE` nhỏ nhất là `0x0101010101010101` nếu là ta đưa từng `feedback` lên để đạt giá trị đó thì sẽ cần đến 72.340.172.838.076.673 lần gọi hàm để đạt giá trị như mong muốn.

Thay vào đó có thể ghi đè sẵn `0xffffffffffffff` vào sẵn (chứa BYTE cuối lại vì ta không muốn NULL BYTE đè lên hàm `viewBalance`). Sau đó dùng `feedback` để cộng thêm giá trị 1 vào. Từ đó, giá trị được nâng lên `0x0100000000000000`. Lặp lại việc ghi đè đến khi đạt đủ `0x0101010101010101`.

Leak binary:
    
    for i in range(7):
        payload=b'A'*16
        payload+=b'\xff'*(7-i)
        p.sendlineafter(b'Choice:',b'3')
        p.sendafter(b'New Description:',payload)
        p.sendlineafter(b'Choice:',b'4')
        p.sendlineafter(b':',b'1')
    
    p.sendlineafter(b'Choice:',b'4')
    p.sendlineafter(b':',b'1')

