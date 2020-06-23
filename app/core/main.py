from starlette.applications import Starlette
from tortoise.contrib.starlette import register_tortoise

from core import settings, urls

app = Starlette(
    debug=settings.DEBUG,
    routes=urls.routes,
    middleware=settings.middleware,
)

# Config ORM Tortoise
# Thiết lập ORM Tortoise
register_tortoise(
    app,
    db_url=str(settings.DATABASE_URL),
    modules={"models": settings.models},
    generate_schemas=True  # for dev
)
