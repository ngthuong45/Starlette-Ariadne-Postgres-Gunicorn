from starlette.routing import Route
from ariadne.asgi import GraphQL

from .settings import schema

#
# Urls của toàn bộ chương trình
routes = [
    Route("/graphql", GraphQL(schema, debug=True)),
]
