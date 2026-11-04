# Quản lí mảng trong bộ nhớ máy tính

<img width="1142" height="690" alt="image" src="https://github.com/user-attachments/assets/24a91e0d-264a-4087-8fa2-923304fe2b1c" />

<br><br>
- Mảng là dải dữ liệu liên tiếp có thể truy cập từng phần tử thông qua index. Index là giá trị được dùng để chương trình tính toán offset rồi cộng vào địa chỉ gốc để đến được 1 phần tử được chỉ định.

nếu mảng arr có địa chỉ ban đầu là `0xffffffffab00` và mỗi phần tử có kích thước 8 BYTES thì:

    arr[0] = 0xffffffffab00 + 0 * 8 = 0xffffffffab00
    arr[1] = 0xffffffffab00 + 1 * 8 = 0xffffffffab08
    arr[2] = 0xffffffffab00 + 2 * 8 = 0xffffffffab10
    ...

# Out of Bounds

- Lỗ hổng *Out of Bounds* phát sinh khi index được nhập vượt ngoài phạm vi của mảng. Chẳng hạn như chương trình cho phép nhập index lớn hơn kích thước thật của mảng hay index là số nguyên có dấu (có thể âm).

- Nhiệm vụ của máy tính chỉ là tính toán địa chỉ qua index và truy cập dữ liệu trong địa chỉ đó. Vậy nên người khai thác lỗ hổng hoàn toàn có thể nhập index ngoài phạm vi mảng để truy cập các dữ liệu quan trọng.

<img width="1050" height="546" alt="image" src="https://github.com/user-attachments/assets/16905c1d-4aa6-4aaf-a278-3e0772c3f2a8" />

# Challenge

[*Video anh trí: Out of Bounds*](https://youtu.be/ogTRLJ3kiIk)

<img width="782" height="582" alt="image" src="https://github.com/user-attachments/assets/0373cd69-dd09-45f7-ad9c-059007bbceaa" />

Chương trình này cho phép nhập Index là số nguyên có dấu. Và bên dưới cũng chỉ có giới hạn `v4` bé hơn 10. Ở đây có lỗ hổng `Out of Bounds` cho phép ta truy cập phần tử vượt phạm vi mảng với Index âm.

<img width="868" height="580" alt="image" src="https://github.com/user-attachments/assets/0cb9d3d7-f080-48d7-a770-f61f570b6710" />

Nhìn vào chương trình thì ta thấy có nhiều câu lệnh truy cập phần tử lúc thì `acc`, lúc thì `qword_3608`. Hãy xem cấu trúc mảng này trên bộ nhớ thế nào.

<img width="697" height="298" alt="image" src="https://github.com/user-attachments/assets/fd0ca8ca-7b8b-4ad0-82df-ef6b0d11cc57" />

