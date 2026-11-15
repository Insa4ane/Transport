from fastapi import APIRouter, Depends

from ..dependencies import get_auth_service
from ..schemas.auth import LoginIn, LoginOut, RegisterIn, UserOut
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterIn, auth: AuthService = Depends(get_auth_service)):
    return auth.register(data.username, data.password, data.is_driver)


@router.post("/login", response_model=LoginOut)
def login(data: LoginIn, auth: AuthService = Depends(get_auth_service)):
    token, user = auth.login(data.username, data.password)
    return LoginOut(access_token=token, user=UserOut.model_validate(user))
