# ============================================================
# 파일 위치: board_api/app/schemas/auth.py
# ============================================================

from pydantic import BaseModel, Field

# 회원가입 request 용
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)
    name:     str = Field(..., min_length=1, max_length=50)

# 회원가입 response용
class UserInfo(BaseModel):
    username: str
    name:     str
    model_config = {"from_attributes": True}

class TokenPair(BaseModel) :
    """
    로그인 성공시 반환되는 토큰 한 쌍 (Access + Refresh Token의 쌍)
    """
    access_token : str,
    refresh_token : str,
    token_type : str = 'bearer'

class AccessTokenOnly(BaseModel) :
    """
    재발급시 응답되는 AccessToken 응답용
    """
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

class RefreshRequest(BaseModel) :
    """
    Refresh 토큰 요청용
    """
    refresh_token : str

class LogoutRequest(BaseModel) :
    """
    로그아웃 요청
    """
    refresh_token : str