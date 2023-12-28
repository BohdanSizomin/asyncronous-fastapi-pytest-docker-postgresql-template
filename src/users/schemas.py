from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


# example for creating user
class UserCreate(UserBase):
    password: str
    username: str


class UserOut(UserBase):
    id: int
    uuid: str

    class Config:
        from_attributes = True
