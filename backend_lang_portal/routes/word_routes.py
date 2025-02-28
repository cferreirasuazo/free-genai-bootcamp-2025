from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from database import get_db
from repositories import WordRepository, GroupRepository
import schemas
from schemas import GroupResponse, PaginatedResponse, WordsImportRequest
from utils.rate_limiter import RateLimiter

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=60)


@router.get("/words/{word_id}", response_model=schemas.Word)
async def get_word(
    request: Request,
    word_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    repo = WordRepository(db)
    word = repo.get_by_id(word_id)
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return word


@router.get("/words", response_model=List[schemas.Word])
async def get_words(
    request: Request,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    repo = WordRepository(db)
    return repo.get_all()


@router.post("/words", response_model=schemas.Word)
async def create_word(
    request: Request,
    word: schemas.WordCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    repo = WordRepository(db)
    return repo.create(**word.model_dump())


@router.put("/words/{word_id}", response_model=schemas.Word)
async def update_word(
    request: Request,
    word_id: int, 
    word: schemas.WordCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    repo = WordRepository(db)
    updated_word = repo.update(word_id, **word.model_dump())
    if updated_word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return updated_word


@router.delete("/words/{word_id}")
async def delete_word(
    request: Request,
    word_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    repo = WordRepository(db)
    if not repo.delete(word_id):
        raise HTTPException(status_code=404, detail="Word not found")
    return {"message": "Word deleted successfully"}


@router.post("/words/import")
async def import_words(
    request: Request,
    import_data: WordsImportRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    word_repo = WordRepository(db)
    group_repo = GroupRepository(db)
    
    # Create a new group with the provided name
    group = group_repo.create(name=import_data.group_name)
    
    imported_words = []
    for word_data in import_data.words:
        # Convert the parts list to JSON format expected by the Word model
        parts = {
            "parts": [
                {
                    "kanji": part.kanji,
                    "romaji": part.romaji
                } for part in word_data.parts
            ]
        }
        
        # Create the word
        word = word_repo.create(
            kanji=word_data.kanji,
            romaji=word_data.romaji,
            english=word_data.english,
            parts=parts
        )
        
        # Add word to group
        group_repo.add_word(group.id, word)
        imported_words.append(word)
    
    return {
        "message": f"Successfully imported {len(imported_words)} words into group '{import_data.group_name}'",
        "group_id": group.id,
        "words_count": len(imported_words)
    }
