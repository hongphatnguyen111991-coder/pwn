# Quản lí mảng trong bộ nhớ máy tính

<img width="1142" height="690" alt="image" src="https://github.com/user-attachments/assets/24a91e0d-264a-4087-8fa2-923304fe2b1c" />

<br><br>
- Mảng là dải dữ liệu liên tiếp có thể truy cập từng phần tử thông qua index. Index dùng để chương trình tính toán offset từ đầu mảng đến 1 phần tử được chỉ định.

nếu arr ( arr[0] ) có địa chỉ là `0xffffffffab00` thì:

    arr[1] = 0xffffffffab00 + 1 * 8 = 0xffffffffab08
    arr[2] = 0xffffffffab00 + 2 * 8 = 0xffffffffab10
    ...

# Out of bound 

<img width="1050" height="546" alt="image" src="https://github.com/user-attachments/assets/16905c1d-4aa6-4aaf-a278-3e0772c3f2a8" />

Lỗ hổng *Out of bound* phát sinh khi index được nhập vượt ngoài phạm vi của mảng. Chẳng hạn như chương trình cho phép nhập index lớn hơn kích thước thật của mảng hay index là số nguyên có dấu (có thể âm).

Nhiệm vụ của máy tính chỉ là tính toán địa chỉ qua index và truy cập dữ liệu trong địa chỉ đó. Vậy nên người khai thác lỗ hổng hoàn toàn có thể nhập index ngoài phạm vi mảng để truy cập các dữ liệu quan trọng.
