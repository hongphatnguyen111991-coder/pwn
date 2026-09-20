# Phần có thể khai thác

<img width="1652" height="580" alt="image" src="https://github.com/user-attachments/assets/7451517e-f34a-49d7-b7c7-e3b55bcf1ecd" />

Hàm Win đã có sẵn và cơ chế bảo vệ PIE tắt để ta có thể ret2win. Phần cần làm sẽ là chuyển hướng tới địa chỉ Win() lấy flag.

<img width="957" height="397" alt="image" src="https://github.com/user-attachments/assets/ef1a8432-7722-4f7a-bc83-edf84c0fe2bb" />

Lỗi buffer overflow nhưng chỉ giới hạn ghi đè không quá 2 byte ra khỏi vùng buffer

<img width="1437" height="695" alt="Screenshot 2026-09-20 221228" src="https://github.com/user-attachments/assets/d42795b3-2f3f-4466-92ba-bbffea2e12ab" />

Ta có thể ghi đè tối đa 2 byte lên saved rbp vậy chuyển hướng bằng stack pivot sẽ chỉ nằm trong phạm vi từ 0x0x7fffffff0000 -> 0x0x7fffffffffff.

Chương trình sau lần nhập đầu sẽ print chuỗi vừa nhập và từ đó nối được địa chỉ nằm trong rbp leak ra để chuyển hướng.

<img width="1330" height="241" alt="image" src="https://github.com/user-attachments/assets/40dcb820-0cd6-44d8-9d68-68159478f39b" />

Vì địa chỉ trong rbp khác với địa chỉ buffer đúng 2 byte nên có thể chuyển hướng quay lại buffer. 
Chương trình sẽ cho ta nhập lại đến khi s[0]=='q' nên lần nhập thứ 2 ta sẽ cần đưa payload chứa địa chỉ đến Win và ghi đè saved rbp địa chỉ buffer
Sau đó dùng địa chỉ ngay sau làm nơi chứa địa chỉ Win()

    win_addr=leak_stack-816            #quay về ô nhớ đầu của buffer
    payload=b'q'*8                     #chứa kí tự q để thoát vòng lặp
    payload+=p64(exe.sym['Win'])       
    payload=payload.ljust(304,b'A')
    payload+=p64(win_addr)[0:2]        #chỉ lấy 2 byte đầu đưa vào payload

Khi chương trình leave,ret ở hàm Call() thì sẽ chuyển hướng đến Win() đọc flag
