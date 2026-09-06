# BUFFER OVERFLOW
## Khái niệm
Buffer Overflow là kĩ thuật làm tràn bộ nhớ bằng cách nhập số BYTE dữ liệu nhiều hơn dung lượng của ô nhớ buffer khiến cho dữ liệu bị ghi đè xuống các ô nhớ khác. Từ đó những người khai thác lỗ hổng có thể ghi đè câu lệnh để chiếm quyền điều khiển hay ép chương trình hoạt động theo mong muốn của họ.

![Alt text](image/buffer-overflow.png)

# Ví dụ (bof1)
![Alt text](image/buffer-overflow0.png)

Chương trình trên có thể cung cấp cho ta quyền điều khiển shell nếu các biến v5 v6 v7 khác 0. Tuy nhiên chương trình chỉ có thể nhập dữ liệu vào buffer nên ta không thể truy cập v5 v6 v7 theo cách thông thường. Nhưng chương trình này có một lỗ hổng có thể khai thác đó là buffer chỉ có thể chứa 16 BYTE. Trong khi đó lệnh read lại đọc tối đa đến 48 BYTE. Nếu nhập quá dữ liệu của buffer thì từ đó ta có thể ghi đè dữ liệu vào v5 v6 v7 bên dưới.

![Alt text](image/buffer-overflow1.png)

Sau khi nhập 40 kí tự A thì dữ liệu đã được ghi đè vào các ô bên dưới buffer (v5 v6 v7) và thỏa điều kiện.
Nhờ đó ta có quyền truy cập shell.

# Pwntool (bof2)
![Alt text](image/buffer-overflow2.png)

Tương tự ở bof1, ta phải ghi đè giá trị vào các biến a b c để lấy quyền điều khiển shell. Nhưng ở chương trình này giá trị phải khớp với điều kiện trong if. Tuy nhiên, trong asm dữ liệu nhập từ bàn phím sẽ bị chuyển thành mã ascii làm lưu trữ sai dữ liệu. 

![Alt text](image/buffer-overflow3.png)

pwntool có thể giúp nhập trực tiếp BYTE thô vào chương trình để đảm bảo dữ liệu được nhập đúng định dạng và kích thước BYTE phù hợp. Giả dụ khi nhập payload += p64(0x13371337) thì dữ liệu sẽ được lưu vào ô nhớ là 0x0000000013371337. Từ đó ta có thể nhập dữ liệu đúng yêu cầu và dành quyền điều khiển shell

![Alt text](image/buffer-overflow4.png)

# Ret2Win (bof3)
![Alt text](image/buffer-overflow5.png)
![Alt text](image/buffer-overflow6.png)

Lệnh tạo shell lần này được để đặt ở hàm win. Vì hàm main không có lệnh nào gọi hàm win nên ta phải truy cập bằng cách khác.
Ta có thể tận dụng lệnh read để ghi đè địa chỉ của hàm win vào stack nơi chứa địa chỉ return (RIP). Từ đó truy cập được hàm win dể tạo shell.
Đây gọi là kĩ thuật Ret2Win

![Alt text](image/buffer-overflow7.png)

Trong pwntool, ta có thể dùng lệnh exe=ELF('./bof3') để phân tích cấu trúc file ELF. Bằng cách này ta có thể dùng lệnh exe.sym['win'] để nạp địa chỉ hàm win tự động mà không cần tìm thủ công.

![Alt text](image/buffer-overflow8.png)

Tuy nhiên có một vấn đề nhỏ. Khi ta dùng call win thì địa chỉ trả về lệnh tiếp theo (RIP) sẽ được đẩy vào stack (8 BYTE) và khi vào hàm sẽ push thêm RBP của hàm cha vào stack (8 BYTE). Tổng là 16 BYTE. Và thnah ghi xmm0 yêu cầu stack chia hết cho 16.
Mà khi sử dụng ret2win để truy cập hàm win thì địa chỉ trả về (RIP) chưa vào giờ được push vào stack. Điều này dẫn tới việc push RBP vào hàm sẽ làm stack chỉ tăng lên tổng là 8 BYTE. Khi địa chỉ stack không chia hết cho 16 thì lệnh movaps xmmword ptr [rsp + 0x50], xmm0 lập tức làm chương trình bị crash (SIGSEGV).

![Alt text](image/buffer-overflow9.png)

Một cách đơn giản để khắc phục điều này là ret2win vào địa chỉ bỏ qua lệnh push RBP.

![Alt text](image/buffer-overflow10.png)
