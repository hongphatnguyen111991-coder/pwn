# Phân tích code

<img width="775" height="178" alt="image" src="https://github.com/user-attachments/assets/67f12b4b-05f4-4641-b818-90d3d465e1f8" />
<img width="732" height="337" alt="image" src="https://github.com/user-attachments/assets/b1d3d113-76ec-4b58-bd6c-39b27a78095c" />
<img width="746" height="380" alt="image" src="https://github.com/user-attachments/assets/4db83061-0ca1-4a4c-81e7-02a757a0b63b" />

Chương trình cho phép lựa chọn nhập dữ liệu tối đa 199 BYTES. Sau đó dữ liệu đó được copy vào biến v7 chỉ có sức chứa 50 BYTES, tạo ra lỗ hổng
*buffer overflow*. 

Chính vì lỗ hổng *buffer overflow* cho phép ta ghi đè xuống các biến bên dưới, nên ta cũng có khả năng ghi đè biến v8. Từ đó mở ra lỗ hổng khác là *format string*
ở lệnh `printf(v8,v7)`.
