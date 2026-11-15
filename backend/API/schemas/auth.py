from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from .. import config

Username = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, min_length=config.USERNAME_MIN, max_length=config.USERNAME_MAX
    ),
]


class RegisterIn(BaseModel):
    username: Username
    password: str = Field(min_length=config.PASSWORD_MIN, max_length=config.PASSWORD_MAX)
    is_driver: bool = False

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > config.MAX_PASSWORD_BYTES:
            raise ValueError(
                f"Hasło jest za długie (maksymalnie {config.MAX_PASSWORD_BYTES} bajty)"
            )
        return value


class LoginIn(BaseModel):
    username: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=config.USERNAME_MAX),
    ]
    password: str = Field(min_length=1, max_length=config.PASSWORD_MAX)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    is_driver: bool


class LoginOut(BaseModel):
    access_token: str
    user: UserOut
