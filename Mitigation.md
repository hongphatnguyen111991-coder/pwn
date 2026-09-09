# PIE
Các hệ điều hành có một cơ chế bảo mật gọi là ASLR (viết tắt của Address Space Layout Randomization) sẽ sắp xếp ngẫu nhiên vị trí các vùng nhớ của dùng cho chương trình khi chạy. Điều này chống lại việc những người khai thác lỗ hổng truy cập Stack, Heap, Libraries (Libc) nằm ở các địa chỉ cố định.

Tuy nhiên mục Code/ Data segment không được sắp địa chỉ ngẫu nhiên bới ASLR, tạo ra lỗ hổng dễ bị khai thác. Và cơ chế bảo mật PIE khắc phục điều đó làm cho địa chỉ Code/ Data segment không còn cố định.

Điều này khiến cho việc sử dụng Gadget và tìm địa chỉ hàm trong chương trình trở nên khó khăn hơn.

# 
