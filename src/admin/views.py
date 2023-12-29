from sqladmin import ModelView

from src.users.models import User


class UsersAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
    ]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
