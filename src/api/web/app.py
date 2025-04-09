from litestar import Litestar

from settings import settings
from api.web.handlers import UserController

app = Litestar(
    debug=settings.DEBUG,
    route_handlers=[
        UserController,
    ],
)
