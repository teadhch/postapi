from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        record = RefreshToken(
            user_id=user_id, token=token, expires_at=expires_at,
            created_at=datetime.now(),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
    
    def get_valid(self, token: str) -> Optional[RefreshToken]:
        """
        토큰이 존재하고 아직 만료되지 않았을 때만 반환합니다.
        만료됐거나 존재하지 않으면 None.
        """
        record = self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if not record:  # 토큰이 같은것이 있는지?
            return None
        if record.expires_at < datetime.now():  # 토큰 만료시간이 아직 안되었냐
            return None
        return record
    
    def delete(self, record: RefreshToken) -> None:
        """재발급(rotation) 또는 로그아웃 시 기존 토큰을 무효화합니다."""
        self.db.delete(record)
        self.db.commit()

    def delete_by_token_string(self, token: str) -> None:
        record = self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if record:
            self.db.delete(record)
            self.db.commit()