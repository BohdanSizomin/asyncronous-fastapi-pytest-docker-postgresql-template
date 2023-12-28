from pydantic import BaseModel, EmailStr


class SignUp(BaseModel):
    email: EmailStr
    password: str


class Login(SignUp):
    pass


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    user_id: int
