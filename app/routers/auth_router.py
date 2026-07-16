# ============================================================
# 파일 위치: board_api/app/routers/auth_router.py
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate, UserInfo, TokenPair
from app.auth.jwt import get_current_username

# main.py 의 FastAPI에 등록할 분리된 라우터 모듈
auth_router = APIRouter(prefix="/auth", tags=["인증"])

def get_auth_service(db:Session = Depends(get_db)) -> AuthService :
    return AuthService(db)

@auth_router.post("/register", response_model=UserInfo, status_code=201, summary="회원가입")
def register(
    data: UserCreate,
    service: AuthService = Depends(get_auth_service)
) :
    return service.register(data)

@auth_router.post("/login", response_model=TokenPair, status_code=200, summary="로그인")
def login(
    # Oauth2PasswordRequestForm : username + password를 form데이터로 받음
    form_data : OAuth2PasswordRequestForm = Depends(), 
    service : AuthService = Depends(get_auth_service)
) :
    return service.login(form_data.username, form_data.password)

@auth_router.get("/me", response_model=UserInfo, summary="내 정보 조회")
def get_me(
    username: str = Depends(get_current_username),
    service : AuthService=Depends(get_auth_service)
) :
    return service.get_user_info(username)