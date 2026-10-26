# Biểu diễn số nguyên không dấu và có dấu

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/c46c6400-98a6-431f-a384-e4c85a3bdd83" />


<br>
<br>

- Số nguyên không dấu sử dụng toàn bộ BITS để biểu thị giá trị nguyên dương vậy nên khả năng lưu trữ số lớn gấp 2 lần số nguyên có dấu.

<br>

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/504e6575-0f93-40b3-9399-7136c18f6b2e" />

<br>
<br>

- Phương pháp bù 2 của số nguyên có dấu sẽ coi giá trị BIT đầu là số âm và các BIT còn lại là dương. Vì giá trị tạo thành của BIT trước luôn lớn
hơn tổng giá trị các BIT sau nên nếu BIT đầu bật thì số tạo thành sẽ luôn là số âm.

- Đánh đổi với khả năng lưu trữ số âm thì giá trị lưu trữ tối đa của số nguyên có dấu chỉ bằng nửa của số nguyên không dấu.

# Integer Overflow - Tràn số nguyên có dấu

[*Video anh Trí*](https://youtu.be/1jLxbOtVzdU?si=xsj-gMZaigbTM4Kg)

Tràn số nguyên có dấu xảy ra khi chương trình cho phép nhập giá trị tối đa vượt quá khả năng lưu trữ của kiểu dữ liệu khiến cho BITS dấu bị thay đổi.

### Ví dụ:

<img width="1716" height="767" alt="image" src="https://github.com/user-attachments/assets/749e0349-a086-4da7-9927-2b2bb9f1175b" />

# Integer Overflow - Lỗi ép kiểu

<img width="1320" height="707" alt="image" src="https://github.com/user-attachments/assets/c9f0cd87-dd82-45ee-b82a-b2bfc57869ed" />

<br>

Lỗi ép kiểu xảy ra khi chương trình ép giá trị lớn bằng kiểu dữ liệu không có sức chứa tương xứng làm cho dữ liệu sai lệch so với giá trị ban đầu.
