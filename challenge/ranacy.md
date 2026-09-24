# Phân tích code
 
 <img width="787" height="606" alt="image" src="https://github.com/user-attachments/assets/012c2e18-28cb-41dd-ac5c-4c0b19162389" />

Lỗi buffer overflow nằm trong hàm vul().
Và vòng for chỉ cho phép thực hiện 5 nằm động trước khi ret.

<img width="1127" height="425" alt="image" src="https://github.com/user-attachments/assets/dcabfb1a-dcdf-4a8a-bd9c-f7d6349fa07e" />

Kiểm tra trong stack thì 24 BYTE cuối có thể ghi đè lần lượt là canary, saved_rbp và saved_rip.
Trong stack không có chỗ để chứa ROPchain gọi system nên cần dùng stack pivot để chuyển hướng đến địa chỉ khác chứa ROPchain.
Phù hợp nhất là leak stack (saved_rbp) để tính offset đến buffer và nhập system 
