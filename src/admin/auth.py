from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.dependencies import get_current_user
from src.auth.schemas import TokenData
from src.auth.services import create_access_token
from src.database import db
from src.logger import log
from src.users.models import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        async with db.Session() as async_session:
            user = await User.authenticate(async_session, email, password)
        if user and user.is_admin:
            access_token: str = create_access_token(TokenData(user_id=user.id))
            request.session.update({"token": access_token})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_user(token)
        log(log.INFO, "User: %s", user)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key="...")
