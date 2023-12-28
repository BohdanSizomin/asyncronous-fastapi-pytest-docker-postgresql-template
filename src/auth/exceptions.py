from fastapi import HTTPException, status


class UserException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserCreationError(UserException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User creation error"


class UserNotFoundException(UserException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class UserAlreadyExistsException(UserException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with such email already exists"


class IncorrectEmailOrPasswordException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Wrong Credentials Provided"


class TokenExpiredException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class TokenAbsentException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is missing"
