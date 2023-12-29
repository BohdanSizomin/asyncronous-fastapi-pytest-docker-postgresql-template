from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr


# example for creating user
class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    uuid: str

    ConfigDict(from_attributes=True)
