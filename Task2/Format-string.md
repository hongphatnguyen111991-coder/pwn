# FORMAT STRING
Lỗ hổng Format String xuất hiện khi hàm in ấn (như printf) nhận chuỗi định dạng trực tiếp từ đầu vào người dùng mà không qua kiểm tra.
## Các dịnh dạng phổ biến:
`%p` - In ra giá trị dưới dạng địa chỉ con trỏ (Hexadecimal) có tiền tố `0x`.

`%x` - In ra số nguyên 32-bit (unsigned int) dạng Hexadecimal.

`%lx` - In ra số nguyên 64-bit (unsigned long) dạng Hexadecimal.

Khác biệt với `%p` , `%x` chỉ in giá trị số đơn thuần (ví dụ ff), còn `%p` sẽ tự động đệm đủ độ dài con trỏ và thêm `0x` ở đầu (ví dụ 0x000000ff).

`%d` - In ra số nguyên có dấu (Signed Integer) dạng hệ 10.

`%u` - In ra số nguyên không dấu (Unsigned Integer) dạng hệ 10.

`%c` - In ra 1 ký tự duy nhất dựa trên mã ASCII.

`%s` - In ra chuỗi ký tự cho tới khi gặp byte Null (\x00).

`%n` - Không in ra dữ liệu, mà thực hiện ghi số lượng byte đã được in ra trước nó vào địa chỉ biến được truyền vào.

    char name[] = "Alice"; // Chuỗi "Alice" có độ dài 5 bytes
    int count = 0;

    // printf in chuỗi "Hello " (6 bytes) + chuỗi name (5 bytes) = 11 bytes
    printf("Hello %s%n\n", name, &count);

    printf("So byte đã in trước %%n là: %d\n", count); 
    // Kết quả in ra: 11
