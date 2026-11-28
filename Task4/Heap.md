# Cấu trúc Allocated chunk

Khi người dùng gọi lệnh `malloch` thì chương trình tạo ra các vùng nhớ gọi là chunk. Các chunk đã được cấp phát và chưa bị freed được gọi là Allocated chunk.

<img width="500" height="378" alt="chunk-allocated-simple-CS" src="https://github.com/user-attachments/assets/416deff2-2f5d-4c95-b85b-e03ccd7da597" />

Mỗi Allocated chunk bao gồm `metadata` và `user data`.

- `metadata`: nơi lưu trữ kich thước của chunk
- `user data`:  nơi lưu trữ dữ liệu mà người dùng nhập vào

<img width="1817" height="812" alt="image" src="https://github.com/user-attachments/assets/28e33630-b6e3-45a6-aa1c-5e777033244f" />


