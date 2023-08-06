__all__ = [
        'Session'
]
from secrets import token_hex
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from dtmodel.base import config

Session = Middleware(SessionMiddleware, secret_key=config.get('SESSION_SECRET', cast=str, default=token_hex()))