import jwt

from users.authentication.auth import LioToken


class Logout(LioToken):

    def __init__(self, request):
        super().__init__()
        self.request = request

    async def deactivate_token(self):
        """
        Hàm dùng cho việc huỷ kích hoạt Token khi người dùng logout
        bằng cách thêm Token vào file blacklist

        :return: object

        ** Lưu ý: hàm cần phải trả về một object khớp với user_type_defs
        trong file Schema dùng cho GraphQL
        """

        if 'Authorization' not in self.request.headers:
            return None

        auth = self.request.headers['Authorization']

        token = self.get_token_from_header(authorization=auth, prefix='lioToken')

        try:
            payload = self.decode_token(token)
        except jwt.InvalidTokenError:
            return {
                'status': False,
                'error': 'Token không hợp lê'
            }
        else:
            with open('security.txt', 'a') as reader:
                reader.write(token + '\n')  # thêm token vào file backlist

            return {
                'status': True,
                'error': None
            }
