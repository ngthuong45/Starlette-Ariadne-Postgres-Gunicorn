from ariadne import QueryType, MutationType
from tortoise.exceptions import DoesNotExist

from ..authentication.login import Login
from ..authentication.logout import Logout
from ..authentication.register import RegisterUser
from ..models import User

user_type_defs = """
    type Query {
        currentUser: UserPayload
    }

    type Mutation {
        createUser(userInput : UserInput!) : createUserPayload
        login(username: String!, password: String!): LoginPayload
        logout: LogoutPayload
    }
    
    type createUserPayload {
        error: String
        user: User
    }
    
    type LoginPayload {
        status: Boolean!
        error: String
        token: String
    }
    
    type UserPayload {
        error: String
        user: User
    }
    
    type LogoutPayload {
        status: Boolean
        error: String
    }

    input UserInput {
        username : String!
        password : String!
        email : String!
        phone : String!
    }

    type User {
        id : ID!
        status: Int!
        username : String!
        password : String!
        email : String!
        phone : String!
    }


"""

user_query = QueryType()
user_mutation = MutationType()


# QUERY
@user_query.field('currentUser')
async def get_current_user_by_id(ojb, info):
    request = info.context['request']
    if request.user.is_authenticated:
        try:
            user = await User.get(pk=request.user.user_id)
        except DoesNotExist:
            return {
                'error': 'user không tồn tại',
            }

        return {
            'user': user
        }


# MUTATION
@user_mutation.field('createUser')
def create_user(obj, info, userInput):
    return RegisterUser(
        username=userInput['username'],
        password=userInput['password'],
        email=userInput['email'],
        phone=userInput['phone']
    ).register()


@user_mutation.field('login')
def user_login(obj, info, username, password):
    info_context = info.context['request']
    return Login(info_context, password, username).verify_user()


@user_mutation.field('logout')
def user_logout(obj, info):
    request = info.context['request']
    if request.user.is_authenticated:
        return Logout(request).deactivate_token()
