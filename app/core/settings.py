from starlette.config import Config
from starlette.datastructures import URL, Secret, CommaSeparatedStrings
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from ariadne import make_executable_schema

from users.authentication.auth import JWTAuthenticationBackend
from users.graphQL.schema import user_type_defs, user_query, user_mutation

# CONFIG ENV
config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
JWT_SECRET_KEY = config('JWT_SECRET_KEY', cast=Secret)
JWT_ALGORITHM = config('JWT_ALGORITHM', cast=Secret)

# CONFIG DATABASE
DATABASE_URL = config('DATABASE_URL', cast=URL)
if TESTING:
    DATABASE_URL = DATABASE_URL.replace(database='test_' + DATABASE_URL.database)

# CONFIG MIDDLEWARE
middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS),
    Middleware(AuthenticationMiddleware,
               backend=JWTAuthenticationBackend(secret_key=str(JWT_SECRET_KEY), algorithm=str(JWT_ALGORITHM),
                                                prefix='lioToken'))
]

# CONFIG APP MODELS
models = [
    'users.models',
]

# CONFIG GRAPHQL
type_defs = [
    user_type_defs,
]

object_types = [
    user_query,
    user_mutation,
]

# Create executable schema instance
schema = make_executable_schema(type_defs, object_types)
