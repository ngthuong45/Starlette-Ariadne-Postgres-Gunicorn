import re
from tortoise.query_utils import Q

from users.models import User
from users.authentication.auth import LioPassword


class RegisterUser:
    def __init__(self, username: str, password: str, email: str, phone: str, status: int = 0):
        self.status = status
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone

    async def register(self):
        """
        Hàm dùng cho việc đăng ký tài khoản người dùng

        :return: object

        ** Lưu ý: hàm cần phải trả về một object khớp với user_type_defs
        trong file Schema dùng cho GraphQL
        """

        email_regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        phone_regex = "^\+?(?:03|05|07|08|09)(?:\d){8}$"  # Các đầu số 03, 05, 07, 08, 09

        user = await User.filter(
            Q(username=self.username) | Q(email=self.email) | Q(phone=self.phone)
        )

        if user:
            return {
                'error': 'Username, Email hoặc Số điện thoại đã tồn tại!',
            }
        elif re.search(email_regex, self.email) is None:
            return {
                'error': 'Email không đúng định dạng!'
            }
        elif re.search(phone_regex, self.phone) is None:
            return {
                'error': 'Số điện thoại không đúng định dạng!'
            }
        else:
            new_user = await User.create(
                status=self.status,
                username=self.username,
                password=LioPassword().hash_password(password=self.password),
                email=self.email,
                phone=self.phone,
            )
            return {
                'user': new_user
            }
