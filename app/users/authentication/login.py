from tortoise.exceptions import DoesNotExist
from datetime import datetime, timedelta

from users.models import User
from users.authentication.auth import LioToken, LioPassword


# Authentication
class Login:
    def __init__(self, info_context, password, username):
        self.info_context = info_context
        self.username = username
        self.password = password

    async def verify_user(self):
        """
        Hàm dùng cho việc xác thực tài khoản khi người dùng login

        :return: object

        ** Lưu ý: hàm cần phải trả về một object khớp với user_type_defs
        trong file Schema dùng cho GraphQL
        """

        try:
            user = await User.get(username=self.username)
        except DoesNotExist:
            return {
                'status': False,
                'error': 'Username khong ton tai !',
            }

        if user.status == 0:
            return {
                'status': False,
                'error': 'Tài khoản của bạn chưa xác thực!',
            }
        elif user.status == 1:
            if LioPassword().match_password(password=self.password, password_in_db=user.password):
                payload = {
                    'userId': user.id,
                    'exp': datetime.utcnow() + timedelta(minutes=30)
                }
                jwt_token = LioToken().encode_token(payload)  # Create a token

                return {
                    'status': True,
                    'token': jwt_token
                }
            else:
                return {
                    'status': False,
                    'error': 'Password khong chinh xac !',
                }
        else:
            return {
                'status': False,
                'error': 'Tài khoản đã bị khoá!',
            }
