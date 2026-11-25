# Phân tích code

<img width="775" height="178" alt="image" src="https://github.com/user-attachments/assets/67f12b4b-05f4-4641-b818-90d3d465e1f8" />
<img width="732" height="337" alt="image" src="https://github.com/user-attachments/assets/b1d3d113-76ec-4b58-bd6c-39b27a78095c" />
<img width="746" height="380" alt="image" src="https://github.com/user-attachments/assets/4db83061-0ca1-4a4c-81e7-02a757a0b63b" />

- Option 1 cho phép nhập dữ liệu tối đa 199 BYTES vào mảng s chứa được 200 BYTES. 
- Option 2 copy dữ liệu vừa nhập vào biến `v7` chỉ có sức chứa 50 BYTES, tạo ra lỗ hổng *buffer overflow*. 
- Option 3 dùng `printf` in dữ liệu với format là `v8` và buffer là `v8`. Vì ta có thể ghi đè `v8` qua lỗ hổng *buffer overflow* nên có thể kiểm soát hoàn toàn format, tạo ra thêm lỗ hổng *format string*

# Mitigation
<img width="815" height="233" alt="image" src="https://github.com/user-attachments/assets/ae73d1c7-e054-4610-aa9c-c8b834abc114" />

## Khai thác
Vì trong chương trình, ta bị kẹt trong vòng lặp while nên ghi đè ret address cũng không thể tạo shell. Cần ghi đè địa chỉ GOT của 1 hàm trong
vòng lặp bằng hàm `system`.

<img width="951" height="326" alt="image" src="https://github.com/user-attachments/assets/63a6a59a-867a-4ed1-9d4b-2453c67e254b" />
<img width="637" height="157" alt="image" src="https://github.com/user-attachments/assets/e3852900-de99-460c-85a9-2c976b7f0750" />

Trong chương trình, hàm `strcpy` có tham số đầu tiên mà ta có thể điều khiển và đưa chuỗi `/bin/sh\0` vào.

## Leak exe, libc

Nhập vào buffer vừa đúng 50 BYTES rồi đưa thêm format để leak 
