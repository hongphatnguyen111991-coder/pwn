# Cấu trúc Allocated chunk

Khi người dùng gọi lệnh `malloch` thì chương trình tạo ra các vùng nhớ gọi là chunk. Các chunk đã được cấp phát và chưa bị freed được gọi là Allocated chunk.

<img width="500" height="378" alt="chunk-allocated-simple-CS" src="https://github.com/user-attachments/assets/416deff2-2f5d-4c95-b85b-e03ccd7da597" />

Mỗi Allocated chunk bao gồm `metadata` và `user data`.

- `metadata`: nơi lưu trữ kich thước của chunk
- `user data`:  nơi lưu trữ dữ liệu mà người dùng nhập vào

Mỗi khi gọi `malloch` thì lệnh sẽ trả về địa chỉ tại vùng nhớ `user data` của chunk. 

<br>

<img width="1865" height="793" alt="image" src="https://github.com/user-attachments/assets/18a96174-98a1-4444-87a8-114459d115a5" />

Mỗi `metadata` gồm 2 phần:

- Previous Chunk Size: kích thước của chunk trước đó.
- Chunk Size: kích thước của chunk hiện tại

VÍ DỤ: Khi chương trình gọi malloch

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
  
    void main(void)
    {
      char *ptr;
      ptr = malloc(0x10);
      strcpy(ptr, "panda");
    }
