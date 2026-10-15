## Phân tích chương trình

<img width="827" height="721" alt="Screenshot 2026-10-15 163019" src="https://github.com/user-attachments/assets/390291f1-e33d-470c-9937-cacfc6ba9999" />

Chương trình tạo shell nếu v6 == v8. Với v6 nhập từ user và v8 được sinh ngẫu nhiên qua công thức.

Để biết giá trị sẽ được generate vào v8, ta sẽ cần seed. Mà seed được tạo bởi `/dev/urandom`. Không giống `time(0)` luôn đồng bộ giữa các thiết bị tại cùng 1 thời điểm.
`/dev/urandom` liên tục xáo trộn bể entropy mỗi lần lấy giá trị và không thể dự đoán.

Vậy chúng ta phải tìm cách khác để tìm seed.

<img width="1202" height="150" alt="Screenshot 2026-10-15 162930" src="https://github.com/user-attachments/assets/2f4e4ca3-fe8d-4dd0-abfc-b55e8a51f350" />

Nhìn vào GDB có thể thấy Seed được lưu trữ vào 4 BYTE của thanh ghi. Tức giới hạn số nguyên của seed là 2^32 - 1.

Nếu ta brute force từng seed từ 0 đến 2^32 - 1 rồi tạo số qua `rand()` đem so sánh với đầu ra của chương trình thì có thể tìm seed chính xác.

Vì chương trình cho phép nhập không giới hạn số lần nên ta hãy dùng 2 lần đầu để lấy đầu ra: 

    data=[]
    for i in range (2):
    p.sendlineafter(b'ID: ',b'1')
    p.recvuntil(b'with ID ')
    temp=int(p.recvline()[:-1])
    data.append(temp)
    p.sendlineafter(b'bksec-er? ',b'Y')

*Lưu ý*: nên lấy ít nhất 2 đầu ra để so sánh vì 1 đầu ra có thể cấu thành từ nhiều seed.

Bây giờ tạo vòng lặp để tìm seed:

    seed=0
    for i in range (2**32):
    	found=1
    	libc.srand(i)
      
    	for j in range(2):
    		test=libc.rand() % 10000 + 20240000
    		if test!=data[j]:
    			found=0
    			break
    
    	if found==1:
    		seed=i
    		break

Sau khi đã tìm thấy seed thì đưa vào sinh số `rand()` và áp công thức trong chương trình.

    libc.srand(seed)
    for i in range (2):
    	dump=libc.rand()
    ID=libc.rand() % 10000 + 20240000
    print(ID)

Ở đây tôi dùng `p.sendlineafter(b'ID: ',p32(ID))` không được nên `print` ra rồi nhập tay vô chương trình luôn :vv

<img width="907" height="632" alt="image" src="https://github.com/user-attachments/assets/6d75c8c6-8a1f-4f68-9dcb-eccf4274331d" />


