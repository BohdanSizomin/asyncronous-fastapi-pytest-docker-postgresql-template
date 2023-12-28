from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_hash(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
