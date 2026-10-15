## Phân tích chương trình

<img width="827" height="721" alt="Screenshot 2026-10-15 163019" src="https://github.com/user-attachments/assets/390291f1-e33d-470c-9937-cacfc6ba9999" />

Chương trình tạo shell nếu v6 == v8. Với v6 nhập từ user và v8 được sinh ngẫu nhiên qua công thức.

Để biết giá trị sẽ được generate vào v8, ta sẽ cần seed. Mà seed được tạo bởi `/dev/urandom`. Không giống `time(0)` luôn đồng bộ giữa các thiết bị tại cùng 1 thời điểm.
`/dev/urandom` liên tục xáo trộn bể entropy mỗi lần lấy giá trị và không thể dự đoán.

Vậy chúng ta phải tìm cách khác để tìm seed.

<img width="1202" height="150" alt="Screenshot 2026-10-15 162930" src="https://github.com/user-attachments/assets/2f4e4ca3-fe8d-4dd0-abfc-b55e8a51f350" />
