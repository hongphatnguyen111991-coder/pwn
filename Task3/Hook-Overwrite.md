# Hook Overwrite
[*Video anh Trí*](https://youtu.be/WxV6Vr4j8bo)

Khi sử dụng Heap thì ta có các hàm `malloch`, `free`, `realloc`. Tương ứng với các hàm đó là các hook `__malloc_hook`, `__free_hook`, `__realloc_hook`.

<img width="1118" height="718" alt="image" src="https://github.com/user-attachments/assets/24cbfc61-0881-47e1-a55d-23d6623aea09" />

<br><br>
Hook là các biến được lưu trữ trong phân vùng Libc. Mỗi khi có các hàm tương tác Heap được gọi thì chương trình sẽ kiểm tra xem biến Hook của hàm đó có phải NULL không. Nếu có thì chương trình sẽ call luôn địa chỉ nằm trong biến hook đó.

# Challenge Dreamhack
[*hook*](https://dreamhack.io/wargame/challenges/52/)

# Phân tích code

<img width="630" height="462" alt="Screenshot 2026-11-10 141415" src="https://github.com/user-attachments/assets/d7eb8542-ce7c-4425-a0c9-c57cddf472fc" />

<br><br>
Trong chương trình đầu tiên tạo ra 1 vùng nhớ Heap với kích thước và dữ liệu nhập từ bàn phím.

## Lỗ hổng cho phép ghi đè
Sau đó cần lưu ý lệnh `*(long *)*ptr = *(ptr+1)`. Về bản chất thì lệnh này lấy 8 BYTES đầu tiên tại ptr để làm đích đến. Sau đó lấy 8 BYTES sau để làm dữ liệu ghi đè lên đích đến đó.

<img width="1702" height="885" alt="image" src="https://github.com/user-attachments/assets/e6a60744-d200-4aad-ab7a-57799badda62" />

Tức ta có thể lợi dùng câu lệnh này để ghi đè lên bất kì địa chỉ nào hợp lệ có trong chương trình.

## Lỗi double free
Tiếp theo thì ở dưới có 2 lệnh free vào cùng vùng nhớ ptr gây ra lỗi double free và crash. Vậy nên dù cuối chương trình có gọi `system('/bin/sh\0')` thì ta cũng không có cách nào truy cập được.

# Khai thác

Ý tưởng khai thác ở đây là ghi đè vào `__free_hook` địa chỉ lệnh `system('/bin/sh')` để tạo shell ngay khi gọi free().

<img width="662" height="182" alt="image" src="https://github.com/user-attachments/assets/3ec2bef9-8d55-4c24-9f8c-b9206f24f13d" />
<img width="1077" height="207" alt="image" src="https://github.com/user-attachments/assets/95101396-eaeb-46c1-ae25-43a872ce923f" />

Chương trình cho ta sẵn địa chỉ libc. Từ đó tính được libc base và địa chỉ `__free_hook`.

Sau


