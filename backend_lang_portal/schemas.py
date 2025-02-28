from pydantic import BaseModel
from typing import List, Optional, Dict, Generic, TypeVar
from datetime import datetime

class WordBase(BaseModel):
    kanji: str
    romaji: str
    english: str
    parts: Dict

class WordCreate(WordBase):
    pass

class Word(WordBase):
    id: int
    
    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    words_count: int

    class Config:
        from_attributes = True

class StudySessionBase(BaseModel):
    group_id: int
    study_activity_id: int

class StudySession(StudySessionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

T = TypeVar('T')

class GroupResponse(BaseModel):
    id: int
    name: str
    words_count: int

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    has_more: bool

class WordReviewCreate(BaseModel):
    word_id: int
    correct: bool

class WordReviewResponse(BaseModel):
    id: int
    word_id: int
    study_session_id: int
    correct: bool
    created_at: datetime

    class Config:
        from_attributes = True 

class WordPart(BaseModel):
    kanji: str
    romaji: List[str]

class WordImport(BaseModel):
    kanji: str
    romaji: str
    english: str
    parts: List[WordPart]

class WordsImportRequest(BaseModel):
    group_name: str
    words: List[WordImport]