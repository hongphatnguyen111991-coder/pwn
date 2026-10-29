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
