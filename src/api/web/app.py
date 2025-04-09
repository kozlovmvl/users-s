from litestar import Litestar

from api.web.settings import settings
from api.web.handlers import UserController

app = Litestar(
    debug=settings.DEBUG,
    route_handlers=[
        UserController,
    ],
)
