from fastapi.routing import APIRoute
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_endpoint_name(route: APIRoute):
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return route.name


def create_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_hash(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
