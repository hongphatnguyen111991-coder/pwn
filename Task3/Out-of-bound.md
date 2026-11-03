# Quản lí mảng trong bộ nhớ máy tính

<img width="1142" height="690" alt="image" src="https://github.com/user-attachments/assets/24a91e0d-264a-4087-8fa2-923304fe2b1c" />

Mảng là dải dữ liệu liên tiếp có thể truy cập từng phần tử thông qua index. Index dùng để chương trình tính toán offset từ đầu mảng đến 1 phần tử được chỉ định.

nếu arr ( arr[0] ) có địa chỉ là `0xffffffffab00` thì:

    arr[1] = 0xffffffffab00 + 1 * 8 = 0xffffffffab08
    arr[2] = 0xffffffffab00 + 2 * 8 = 0xffffffffab08
    ...


