import jwt

from passlib.context import CryptContext
from starlette.authentication import (BaseUser, AuthenticationBackend, AuthenticationError, AuthCredentials,
                                      UnauthenticatedUser)

from core import settings


class JWTUser(BaseUser):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> int:
        return self.user_id

    @property
    def identity(self) -> int:
        return self.user_id


class LioPassword:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])  # Hash password

    def match_password(self, password: str, password_in_db: str):
        """
        Hàm dùng cho việc so sánh xác thực mật khẩu

        :param password: mật khẩu dùng để so sánh
        :param password_in_db: mật khẩu được lấy từ Database
        :return: True hoặc False
        """

        return self.pwd_context.verify(password, password_in_db)

    def hash_password(self, password: str):
        """
        Hàm dùng cho việc mã hoá mật khẩu

        :return: chuỗi sau khi được mã hoá
        """

        return self.pwd_context.hash(password)


class LioToken:
    def __init__(self):
        self.JWT_SECRET_KEY = str(settings.JWT_SECRET_KEY)
        self.JWT_ALGORITHM = str(settings.JWT_ALGORITHM)

    def encode_token(self, payload: dict):
        """
        Hàm dùng cho việc mã hoá Token

        :param payload: là một Dict các thông tin cần truyền vào Token
        :return: Token string
        """

        jwt_token = jwt.encode(payload, self.JWT_SECRET_KEY, self.JWT_ALGORITHM)
        return jwt_token.decode('utf-8')

    def decode_token(self, token: str):
        """
        Hàm dùng cho việc giải mã Token

        :param token: chuỗi Token
        :return: một Dict Payload được truyền vào khi mã hoá
        """

        return jwt.decode(token, self.JWT_SECRET_KEY, self.JWT_ALGORITHM)

    @staticmethod
    def get_token_from_header(authorization: str, prefix: str):
        """
        Hàm dùng cho việc lấy ra Token từ một
        chuỗi Authorization có trong request headers

        :param authorization: chuỗi Authorization có trong request headers
        :param prefix: tiếp đầu ngữ của chuỗi Authorization, mặc định là "lioToken"
        :return: chuỗi Token
        """

        try:
            scheme, token = authorization.split()
        except ValueError:
            raise AuthenticationError('Could not separate Authorization scheme and token')
        if scheme != prefix:
            raise AuthenticationError(f'Authorization scheme {scheme} is not supported')
        return token


class JWTAuthenticationBackend(AuthenticationBackend, LioToken):
    def __init__(self, secret_key: str, prefix: str, algorithm: str):
        super().__init__()
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.prefix = prefix

    async def authenticate(self, request):
        """
        Hàm dùng cho việc xác thực Http Request từ client

        :param request: HTTP request từ client
        :return: authenticated và JWTUser
        """

        if 'Authorization' not in request.headers:
            return None

        auth = request.headers['Authorization']
        token = self.get_token_from_header(authorization=auth, prefix=self.prefix)

        try:
            payload = self.decode_token(token)
        except jwt.InvalidTokenError:
            raise AuthenticationError('error: Token không hợp lệ!')
        else:
            # Kiểm tra xem Token có nằm trong danh sách blacklist Token hay không
            # ** blacklist Token là file chứa danh sách các token đã logout hoặc đã bị vô hiệu hóa
            with open('security.txt', 'r') as reader:
                modify_token_for_check = token + '\n'
                if modify_token_for_check in reader.readlines():
                    raise AuthenticationError('error: Token đã bị vô hiệu hoá!')
                else:
                    return AuthCredentials(['authenticated']), JWTUser(user_id=payload['userId'])
