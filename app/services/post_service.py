# ============================================================
# 파일 위치: board_api/app/services/post_service.py
# 역할: 비즈니스 로직을 처리합니다.
#       페이징 계산, 조회수 증가, 404 검증 등이 여기 있습니다.
#       DB 접근은 Repository에 위임합니다.
# ============================================================

import math
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

class PostService :
    def __init__(self, db:Session):
        pass
    
    def create_post(self) :
        print("게시판 글 등록!!!! 서비스단!!!!!")