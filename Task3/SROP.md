# Phân tích challenge

<img width="554" height="148" alt="image" src="https://github.com/user-attachments/assets/5db8648f-23f0-4de1-91fc-a40447e99759" />
<img width="598" height="184" alt="image" src="https://github.com/user-attachments/assets/311af485-782d-44a9-8dc5-09fcb100932a" />

Lỗ hổng:

Chương trình có lỗi *buffer overflow* cho phép nhập 1208 (0x500) BYTES. 

Cơ chế bảo vệ:

*No Canary* cho phép ghi đè dữ liệu tự do trong Stack không bị kiểm duyệt

*No PIE* làm cho địa chỉ binary tĩnh

