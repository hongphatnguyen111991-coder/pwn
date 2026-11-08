# Lớp bảo vệ Seccomp
[*Video anh Trí - Lớp bảo vệ Seccomp*](https://www.youtube.com/watch?v=nrKNHrEouUU&list=PLEvZsp0uc3SFuVi6TtcahxqsEbV29lXAM&index=26)


*Seccomp* là một tính năng bảo mật của Linux Kernal, làm giới hạn các hàm syscall có thể gọi trong chương trình.

Khi kiểm tra *seccomp* thì sử dụng lệnh:
  
    seccomp-tools dump ./file

<img width="684" height="284" alt="Screenshot 2026-11-08 141410" src="https://github.com/user-attachments/assets/332cbcd8-3fdf-4bfd-986c-7187e1a5c059" />

Tại đây ta thấy các hàm trong syscall được phép gọi sẽ hiện thị như trên (White-list). Tất cả các lệnh gọi syscall khác sẽ mặc định bị chặn thực thi.

# Challenge Dreamhack
[*seccomp*](https://dreamhack.io/wargame/challenges/59)




