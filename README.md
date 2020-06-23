# Dockerizing Starlette với Postgres, Gunicorn, Ariadne

### Giới thiệu dự án
Dự án demo Web Serviec API Graphql bằng ngôn ngữ lập trình Python có các tính năng: Authen, Register, Login, Logout

Các thư viện chính sử dụng trong dự án
- [Starlette](https://www.starlette.io/) là một lightweight ASGI framework của Python
- [Ariadne](https://ariadnegraphql.org/) cho API GraphQL
- Sử dụng JSON Web Tokens cho xác thực người dùng với thư viện [PyJWT](https://pyjwt.readthedocs.io/en/latest/)
- [passlib](https://pypi.org/project/passlib/) cho việc Hash password người dùng
- [tortoise](https://github.com/tortoise/tortoise-orm) cho việc tương tác ORM với Postgres

Một số điểm lưu ý:
- Khi đăng ký người dùng mới, người dùng sẽ có status=0 điều này có ý nghĩa là user cần phải xác thực
(mục đích là để sau này, ta có thể xác thực người dùng thật qua email hoặc SMS điện thoại)
- Khi người dùng đã xác thực, status người dùng được cập nhật = 1. Bạn kết nối với database và sửa status người dùng từ [0]() thàng [1]() để test các trường hợp login, logout, get user...
- Mỗi khi bạn logout, token sẽ được đưa vào file security.txt. Việc này là để check user đã đăng xuất hay chưa ở backend nếu như frontend không xử lý.

Các tính năng cần có để hoàn thiện hơn:
- Xác thực người dùng thật qua email hoặc SMS điện thoại
- Cập nhật status người dùng khi đã xác thực
- Lên lịch cho việc xóa tất cả các token đã được lưu trong file securtiry.txt

### Development

Sử dụng Starlette cho môi trường development.

1. Thay đổi POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD trong file ".env" và ".env.db"
theo ý của bạn
1. Build và run file docker-compose:

    ```sh
    $ docker-compose up -d --build
    ```

    Kiểm tra web tại: [http://localhost:8000/graphql](http://localhost:8000/graphql).