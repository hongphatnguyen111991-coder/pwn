# Cấu trúc Allocated chunk

Khi người dùng gọi lệnh `malloch` thì chương trình tạo ra các vùng nhớ gọi là chunk. Các chunk đã được cấp phát và chưa bị `free` được gọi là Allocated chunk.

<img width="500" height="378" alt="chunk-allocated-simple-CS" src="https://github.com/user-attachments/assets/416deff2-2f5d-4c95-b85b-e03ccd7da597" />

Mỗi Allocated chunk bao gồm `metadata` và `user data`.

- `metadata`: nơi lưu trữ kich thước của chunk
- `user data`:  nơi lưu trữ dữ liệu mà người dùng nhập vào

Mỗi khi gọi `malloch` thì lệnh sẽ trả về địa chỉ tại vùng nhớ `user data` của chunk. 

<br>

<img width="1865" height="793" alt="image" src="https://github.com/user-attachments/assets/18a96174-98a1-4444-87a8-114459d115a5" />

Mỗi chunk có 1 vùng gọi là `metadata` nằm trước `user data` 0x10 BTYES gồm:

- Previous Chunk Size: kích thước của chunk trước đó. (Vùng Previous Chunk Size vốn được khởi tạo nằm ở cuối chunk trước đó) 
- Chunk Size: kích thước của chunk hiện tại

<br>

### VÍ DỤ: Khi chương trình gọi malloch

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
  
    void main(void)
    {
      char *ptr;
      ptr = malloc(0x10);
      strcpy(ptr, "panda");
    }

### Allocated chunk:

    0x555555559250:    0x0    0x21
    0x555555559260:    0x61646e6170    0x0

Kích thước chunk trước bằng 0x0.  Kích thước chunk hiện tại là 0x21, khác với câu lệnh yêu cầu (0x10).

Điều này là do cách tính size cảu chunk dựa vào tổng của:

- 0x10 BYTES cho `metadata`
- Kích thước được yêu cầu
- bit cờ đánh dấu xem chunk liền trước đó có đang được sử dụng hay đã được giải phóng.

        0x1:     Previous in Use     - Specifies that the chunk before it in memory is in use
        0x2:    Is MMAPPED               - Specifies that the chunk was obtained with mmap()
        0x4:     Non Main Arena         - Specifies that the chunk was obtained from outside of the main arena
