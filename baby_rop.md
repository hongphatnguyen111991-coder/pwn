# Leak địa chỉ 
Kiểm tra việc nối địa chỉ saved RBP trong hàm loop

<img width="1475" height="676" alt="Screenshot 2026-09-13 123000" src="https://github.com/user-attachments/assets/3da9a782-ce25-4d2f-b6f0-f6c35c92aecf" />

Không thể tự gọi syscall vì không có gadget mov rax

<img width="1416" height="1062" alt="Screenshot 2026-09-13 150123" src="https://github.com/user-attachments/assets/8d346ccb-5dc7-41dc-a077-db2ff411a187" />

Có thể thử đưa shellcode vào vùng .BSS. Để làm được điều đó cần có địa chỉ của 1 vùng nhớ trống để ghi đè shellcode vào trong khi PIE đang bật.
Có thể tính offset saved_rbp đến địa chỉ được chọn.

<img width="1392" height="597" alt="Screenshot 2026-09-13 150542" src="https://github.com/user-attachments/assets/e3ef4606-cd92-4ba2-81f7-76b7d42a73c7" />

<img width="1232" height="445" alt="Screenshot 2026-09-13 153743" src="https://github.com/user-attachments/assets/2fb39af0-604d-486e-9fbb-7fa9385e4f79" />

Bây giờ cần nhập shellcode vào địa chỉ
