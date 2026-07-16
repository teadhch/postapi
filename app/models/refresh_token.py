# ============================================================
# 파일 위치: board_api/app/models/refresh_token.py
# ============================================================

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class RefreshToken(Base):
    """
    Refresh Token 저장 테이블.

    DB에 저장하는 이유: 로그아웃 시 즉시 무효화할 수 있어야 하기 때문입니다.
    Access Token(JWT)은 서명만으로 검증하므로 한번 발급하면
    서버가 강제로 무효화할 방법이 없습니다.
    Refresh Token은 DB 레코드이므로 삭제하면 그 즉시 못 쓰게 됩니다.
    """
    __tablename__ = "refresh_token"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    user_id    = Column(Integer, ForeignKey("user.id"), nullable=False)
    token      = Column(String(255), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)