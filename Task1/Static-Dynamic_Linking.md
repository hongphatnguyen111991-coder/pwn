# Static Linking
Hầu hết các chương trình cần chạy các hàm từ thư viện hệ thống, và các hàm thư viện này cũng cần được tải. Trong trường hợp đơn giản nhất, các hàm thư viện cần thiết được nhúng trực tiếp vào tệp nhị phân thực thi của chương trình. Một chương trình như vậy được liên kết tĩnh với các thư viện của nó, và mã thực thi được liên kết tĩnh có thể bắt đầu chạy ngay sau khi được tải.

*Liên kết tĩnh được thực hiện trong quá trình biên dịch chương trình nguồn.*

*Mỗi chương trình được tạo ra phải chứa các bản sao của chính xác các hàm thư viện hệ thống chung.*
 
# Dynamic Linking
Mỗi chương trình liên kết động đều chứa một hàm liên kết tĩnh nhỏ được gọi khi chương trình khởi chạy. Hàm tĩnh này chỉ ánh xạ thư viện liên kết vào bộ nhớ và chạy mã mà hàm chứa. Thư viện liên kết xác định tất cả các thư viện động mà chương trình yêu cầu cùng với tên của các biến và hàm cần thiết từ các thư viện đó bằng cách đọc thông tin có trong các phần của thư viện. Sau đó, nó ánh xạ các thư viện vào giữa bộ nhớ ảo và giải quyết các tham chiếu đến các ký hiệu có trong các thư viện đó. 

*Một DLL chỉ được tải vào bộ nhớ một lần, trong khi nhiều ứng dụng có thể sử dụng cùng một DLL tại một thời điểm, do đó tiết kiệm không gian bộ nhớ.*
