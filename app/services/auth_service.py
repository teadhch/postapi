# ============================================================
# 파일 위치: board_api/app/services/auth_service.py
# ============================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.auth.jwt import (hash_password, 
                          verify_password, 
                          create_access_token,
                          generate_refresh_token,
                          generate_refresh_token_expiry)
from app.schemas.auth import UserCreate, UserInfo, TokenPair


class AuthService :
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.refresh_repo = RefreshTokenRepository
        # refresh_repo는 로그인 단계에서 추가합니다
    
    def register(self, data: UserCreate) -> UserInfo:
        """
        회원가입.
        1. 아이디 중복 검사 (Repository 조회)
        2. 비밀번호 해싱 (app.auth.jwt)
        3. 저장 (Repository)
        """
        if self.user_repo.get_by_username(data.username):
            raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")

        user = self.user_repo.create(
            username=data.username,
            hashed_password=hash_password(data.password),
            name=data.name,
        )
        return UserInfo.model_validate(user)
    
    def login(self, username:str, password:str) -> TokenPair :
        """
        로그인 성공 시 Access Token + Refresh Token 두 개를 함께 발급합니다.
        Refresh Token은 DB에 저장해서 나중에 무효화할 수 있게 합니다.
        """
        user = self.user_repo.get_by_username(username)

        if not user or not verify_password(password, user.hashed_password) :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = "아이디 또는 비밀번호가 올바르지 않습니다"
                headers = {"WWW-Authorized" : "Bearer"}
            )

        # 로그인한 사용자의 id(username)을 access_token에 넣어 발급
        access_token = create_access_token(data = {"sub" : user.username})

        # refresh_token 발급
        refresh_token = generate_refresh_token()

        # Refresh Token을 Db에 저장 (나중에 대조 또는 무효화 하기 위해)
        self.refresh_repo.create(
            user_id=user.id,
            token=refresh_token,
            expires_at=generate_refresh_token_expiry()
        )
        return TokenPair(access_token=access_token, refresh_token=refresh_token)