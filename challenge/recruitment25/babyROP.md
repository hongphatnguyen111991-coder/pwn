# Phân tích code
<img width="852" height="331" alt="image" src="https://github.com/user-attachments/assets/9726f692-dd21-4a0d-ab11-ec1ff253cd85" />

Trong chương trình này có lỗ hổng *buffer overflow*. Bên dưới có kiểm duyệt độ dài chuỗi nhưng có thể bypass bằng cách nhập NULL BYTE giữa payload.

## Mitigation
<img width="808" height="277" alt="image" src="https://github.com/user-attachments/assets/259b0241-6c6b-4011-8942-4f79c46c20fc" />

No PIE nên các địa chỉ binary cố định để khai thác.

## Gadget
<img width="808" height="277" alt="image" src="https://github.com/user-attachments/assets/8575d217-ae6b-4262-886e-b8a50fba72af" />
