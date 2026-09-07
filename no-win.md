# TÌM PHƯƠNG PHÁP
<img width="665" height="297" alt="image" src="https://github.com/user-attachments/assets/c955af93-b0b6-4f5a-a3d6-580ed020dd69" />

=>buffer overflow (có vẻ hơi rõ ràng)

<img width="421" height="187" alt="image" src="https://github.com/user-attachments/assets/4a40a548-a0ea-4a24-b63c-868633563682" />

Bảo mật NX đang bật, không thể thực thi ở vùng nhớ stack. Phải thông qua lệnh ở vùng .text  
=>ROPchain

# TÌM GADGET
<img width="495" height="152" alt="image" src="https://github.com/user-attachments/assets/2e4c8878-9d41-435d-9f44-b88b41123d6c" />

vì `pop rdi/rsi ; pop rbp ; ret` bị dư rbp ở đằng sau, ta sẽ cần chèn thêm 8 byte rác để pop rbp không ảnh hưởng đến việc nhập dữ liệu vào các thanh ghi khác

# setup ghi /bin/sh vào ô nhớ tĩnh và syscall 59
<img width="352" height="166" alt="image" src="https://github.com/user-attachments/assets/47722352-dd84-46a0-8c81-3016bd10d446" />

Vì sau hàm sau hàm read là leave và ta không muốn lệnh bị chuyển hướng đến nơi khác. Nên dùng ret2win để jmp tới hàm read sẽ giúp ta chuyển hướng trực tiếp đến lệnh tiếp theo trên đỉnh stack. Cách này là khả thi vì chế độ bảo mật PIE đang tắt và địa chỉ hàm read là cố định.

<img width="422" height="442" alt="image" src="https://github.com/user-attachments/assets/815b7388-2619-414a-854a-e3e5058a4a70" />

Luồng thực thi bây giờ sẽ là 1 chuỗi các gadget liên tục thay vì bị ngắt do hàm read

