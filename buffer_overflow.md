# BUFFER OVERFLOW
## Khái niệm
Buffer Overflow là kĩ thuật làm tràn bộ nhớ bằng cách nhập số byte dữ liệu nhiều hơn dung lượng của ô nhớ buffer khiến cho dữ liệu bị ghi đè xuống các ô nhớ khác. Từ đó những người khai thác lỗ hổng có thể ghi đè câu lệnh để chiếm quyền điều khiển hay ép chương trình hoạt động theo mong muốn của họ.

![Alt text](image/buffer-overflow.png)

## Ví dụ
![Alt text](image/buffer-overflow0.png)

Chương trình trên có thể cung cấp cho ta quyền điều khiển shell nếu các biến v5 v6 v7 khác 0. Tuy nhiên chương trình chỉ có thể nhập dữ liệu vào buffer nên ta không thể truy cập v5 v6 v7 theo cách thông thường.
Chương trình này có một lỗ hổng có thể khai thác đó là buffer chỉ có thể chứa 16 BYTE. Trong khi đó lệnh read lại đọc tối đa đến 48 BYTE.
Nếu nhập quá dữ liệu của buffer thì từ đó ta có thể ghi đè dữ liệu vào v5 v6 v7 bên dưới.

![Alt text](image/buffer-overflow1.png)

Sau khi nhập 40 kí tự A thì dữ liệu đã được ghi đè vào các ô bên dưới buffer (v5 v6 v7) và thỏa điều kiện.
Nhờ đó ta có quyền truy cập shell
