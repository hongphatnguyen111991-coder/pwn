# PIE
Các hệ điều hành có một cơ chế bảo mật gọi là ASLR (viết tắt của Address Space Layout Randomization) sẽ sắp xếp ngẫu nhiên vị trí các vùng nhớ của dùng cho chương trình khi chạy. Điều này chống lại việc những người khai thác lỗ hổng truy cập Stack, Heap, Libraries (Libc) nằm ở các địa chỉ cố định.

Tuy nhiên mục Code/ Data segment không được sắp địa chỉ ngẫu nhiên bới ASLR, tạo ra lỗ hổng dễ bị khai thác. Và cơ chế bảo mật PIE khắc phục điều đó làm cho địa chỉ Code/ Data segment không còn cố định.

Điều này khiến cho việc sử dụng Gadget và tìm địa chỉ hàm trong chương trình trở nên khó khăn hơn.

# NX
Khi cơ chế NX bật thì các địa chỉ thuộc vùng Stack/Heap sẽ được gắn cờ read/write only và không thể thực thi. Khi người khai thác lỗ hổng chèn shellcode vào vùng Stack thì sẽ từ chối thực thi và dừng chương trình.

# Canary
Cơ chế bảo vệ Canary là cơ chế giúp phát hiện và ngăn chặn các cuộc tấn công bằng buffer overflow nhắm vào return address.

Khi bật Canary, chương trình sẽ chèn thêm một giá trị ngẫu nhiên gọi là Canary vào trước return address. Trước khi thực hiện ret, chương trình sẽ kiểm tra xem giá trị đó có bị thay đổi hay không. Nếu có, chương trình sẽ bị ngắt để tránh việc quyền điều khiển bị chiếm.

Đặc điểm của Canary: Nằm ngay trước saved rbp và BYTE cuối là NULL BYTE
