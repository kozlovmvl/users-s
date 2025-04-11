from litestar import Litestar

from api.web.handlers import UserController
from settings import settings

app = Litestar(
    debug=settings.DEBUG,
    route_handlers=[
        UserController,
    ],
)
