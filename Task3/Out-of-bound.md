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
<br><br>

<img width="868" height="580" alt="image" src="https://github.com/user-attachments/assets/0cb9d3d7-f080-48d7-a770-f61f570b6710" />

Nhìn vào chương trình thì ta thấy có nhiều câu lệnh truy cập phần tử lúc thì `acc`, lúc thì `qword_3608`. Hãy xem cấu trúc mảng này trên bộ nhớ thế nào.
<br><br>

<img width="697" height="298" alt="image" src="https://github.com/user-attachments/assets/fd0ca8ca-7b8b-4ad0-82df-ef6b0d11cc57" />

`acc` và `qword_3608` cùng nằm trong `.BSS` và cách nhau 8 BYTES. Đây là 1 mảng với các phần tử là struct gồm name và amounts:
<br><br>

<img width="1090" height="756" alt="image" src="https://github.com/user-attachments/assets/29960c81-d568-4de6-ae16-95d7fa68ebb1" />

<br><br>
Để dễ dàng đọc IDA thì hãy tạo 1 struct và gán cho mảng `acc`.
<br><br>

<img width="796" height="630" alt="image" src="https://github.com/user-attachments/assets/6b5b1bb1-e197-4ddf-b3f5-52b13187919e" />
<img width="930" height="782" alt="image" src="https://github.com/user-attachments/assets/9143195d-a966-44c0-86bb-4c7220b588c8" />
<img width="860" height="569" alt="Screenshot 2026-11-04 172227" src="https://github.com/user-attachments/assets/a15c5470-c485-4c27-a8f0-9ffee0718edd" />
<img width="552" height="342" alt="Screenshot 2026-11-04 172518" src="https://github.com/user-attachments/assets/97bb28ea-d041-4485-92b5-41144c461ae5" />

Tại đây thì nhấn nút `Y` để tạo biến name và amounts tại 2 địa chỉ trên.

<img width="1000" height="601" alt="image" src="https://github.com/user-attachments/assets/b4d799aa-66b3-4e50-9505-d25c49e94e53" />

Lúc này thì click vào địa chỉ từng biến và ấn `D` đến khi 2 biến trở thành kích thước 8 BYTES.

<img width="714" height="408" alt="image" src="https://github.com/user-attachments/assets/f3e8c046-7c04-4c0a-a223-6fef7e33986c" />

Rồi quay lại mục code C để đổi kiểu dữ liệu mảng acc thành struct Accounts vừa tạo.

<img width="870" height="562" alt="image" src="https://github.com/user-attachments/assets/e2083d97-3e0b-416c-b7c7-8ce0df80a805" />

<br><br>
Nhìn lại chương trình thì ta có hàm `get_shell`. Vậy việc còn lại hiện tại chỉ là điều hướng chương trình đến `get_shell`.

<img width="606" height="208" alt="image" src="https://github.com/user-attachments/assets/02873b01-7943-41e7-81e5-7b43685c60da" />

PIE hiện đang bật nên cần leak địa chỉ binary trước.

<img width="1012" height="602" alt="image" src="https://github.com/user-attachments/assets/e52f6902-d86d-471b-8f80-8e0fe572524f" />

Bên trên `acc` thì có 1 địa chỉ của `__dso_handle` là con trỏ đến chính nó và cũng là địa chỉ binary.

<img width="601" height="350" alt="image" src="https://github.com/user-attachments/assets/d0c689a5-90a7-481e-b97d-2f6fb05650d5" />

Lúc này nếu chuyển luồng thực thi đến lệnh in thì sẽ leak được giá trị trong con trỏ.

<img width="636" height="302" alt="image" src="https://github.com/user-attachments/assets/544abd6a-5b8a-4f5d-bd30-df95d9366691" />

    input()
    p.sendlineafter(b'> ',b'1')
    p.sendlineafter(b'Index: ',b'-5')
    p.sendlineafter(b'> ',b'4')
    p.recvuntil(b'Name: ')
    binary_leak=u64(p.recv(6)+b'\x00\x00')
    exe.address=binary_leak-0x35b0

<img width="982" height="518" alt="image" src="https://github.com/user-attachments/assets/f72c4e13-6b08-491d-a098-7c0c1cd94727" />

Nhìn xa hơn về trước mảng acc thì còn lưu cả các hàm thư viện. Điều này là do cơ chế bảo mật RELRO đang ở trạng thái NO RELRO. Do đó bảng GOT nằm hoàn toàn trong
vùng có quyền `rw-`. 

Vậy chỉ cần ghi đè địa chỉ trong bảng GOT thành `get_shell` để chuyển hướng tạo shell. Ở đây thì ta thường sẽ chọn hàm `exit` vì hàm này sẽ chỉ được gọi cuối chương trình, khi ta đã hoàn thành việc khai thác.

<img width="982" height="518" alt="Screenshot 2026-11-04 180755" src="https://github.com/user-attachments/assets/65f278c7-4bdf-41e6-baf7-f8177ca33778" />











