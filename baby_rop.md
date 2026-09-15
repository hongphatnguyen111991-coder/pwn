# Xây dựng ROPchain
![Uploading Screenshot 2026-09-15 214259.png…]()

Để bypass PIE thì cần leak 1 dịa chỉ tại phân cùng nằm trong .text 

Trong vùng buffer có thể ghi đè có 1 địa chỉ trong phân vùng CODE có thể được leak khi nối vào chuỗi khi print
<img width="1462" height="707" alt="Screenshot 2026-09-15 213406" src="https://github.com/user-attachments/assets/b724ed4a-4d6a-48d2-91c5-257b77e91cfd" />

Khi đã có địa chỉ leak_CODE thì có thể tính base qua công thức:

    leak_main= leak_CODE + offset đến main
    base= leak_main - exe.sym['main']

Sử dụng base address này để tính
    

