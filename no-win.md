# TÌM PHƯƠNG PHÁP
<img width="665" height="297" alt="image" src="https://github.com/user-attachments/assets/c955af93-b0b6-4f5a-a3d6-580ed020dd69" />

=>buffer overflow (có vẻ hơi rõ ràng)

<img width="421" height="187" alt="image" src="https://github.com/user-attachments/assets/4a40a548-a0ea-4a24-b63c-868633563682" />

Bảo mật NX đang bật, không thể thực thi ở vùng nhớ stack. Phải thông qua lệnh ở vùng .text  
=>ROPchain

# TÌM GADGET
<img width="495" height="152" alt="image" src="https://github.com/user-attachments/assets/2e4c8878-9d41-435d-9f44-b88b41123d6c" />

vì ' pop rdi/rsi ; pop rbp ; ret ' bị dư rbp ở đằng sau, ta sẽ cần chèn thêm 8 byte rác để pop rbp không ảnh hưởng đến việc nhập dữ liệu vào các thanh ghi khác
