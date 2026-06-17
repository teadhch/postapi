from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PostCreate(BaseModel) :
    """
    게시글 글 작성 요청 스키마 (body)
    """
    title:str = Field(..., min_length=1, max_length=200, description="글제목")
    content:str = Field(..., min_length=1, description="글내용")
    author:str = Field(..., min_length=1, max_length=12, description="작성자")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI MVC 게시판",
                "content": "Repository, Service, Router로 분리해 작성합니다.",
                "author": "홍길동"
            }
        }
    }

class PostDetail(BaseModel):
    """상세 조회 응답 (본문 포함)"""
    id:         int
    title:      str
    content:    str
    author:     str
    view_count: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}    # 위 속성(attributes)들을 json구조로 출력함