from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from repositories import WordRepository, GroupRepository
import schemas
from schemas import GroupResponse, PaginatedResponse

router = APIRouter()

@router.get("/words/{word_id}", response_model=schemas.Word)
def get_word(word_id: int, db: Session = Depends(get_db)):
    repo = WordRepository(db)
    word = repo.get_by_id(word_id)
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return word

@router.get("/words", response_model=List[schemas.Word])
def get_words(db: Session = Depends(get_db)):
    repo = WordRepository(db)
    return repo.get_all()

@router.post("/words", response_model=schemas.Word)
def create_word(word: schemas.WordCreate, db: Session = Depends(get_db)):
    repo = WordRepository(db)
    return repo.create(**word.model_dump())

@router.put("/words/{word_id}", response_model=schemas.Word)
def update_word(word_id: int, word: schemas.WordCreate, db: Session = Depends(get_db)):
    repo = WordRepository(db)
    updated_word = repo.update(word_id, **word.model_dump())
    if updated_word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return updated_word

@router.delete("/words/{word_id}")
def delete_word(word_id: int, db: Session = Depends(get_db)):
    repo = WordRepository(db)
    if not repo.delete(word_id):
        raise HTTPException(status_code=404, detail="Word not found")
    return {"message": "Word deleted successfully"}

