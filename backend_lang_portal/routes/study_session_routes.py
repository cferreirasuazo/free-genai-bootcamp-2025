from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models import StudySession, Group, StudyActivity
from schemas import StudySessionBase, StudySession as StudySessionSchema, WordReviewCreate, WordReviewResponse
from repositories import StudySessionRepository, WordReviewItemRepository
from utils.rate_limiter import RateLimiter

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=60)

@router.post("/study_sessions", response_model=StudySessionSchema)
async def create_study_session(
    request: Request,
    study_session: StudySessionBase,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    # Validate group exists
    group = db.query(Group).filter(Group.id == study_session.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Validate study activity exists
    activity = db.query(StudyActivity).filter(StudyActivity.id == study_session.study_activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Study activity not found")
    
    # Create new study session
    db_study_session = StudySession(
        group_id=study_session.group_id,
        study_activity_id=study_session.study_activity_id
    )
    
    # Add and commit to database
    db.add(db_study_session)
    db.commit()
    db.refresh(db_study_session)
    
    return db_study_session

@router.post("/study_sessions/{session_id}/review", response_model=WordReviewResponse)
async def create_review(
    request: Request,
    session_id: int,
    review: WordReviewCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    session_repo = StudySessionRepository(db)
    session = session_repo.get_by_id(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
        
    review_repo = WordReviewItemRepository(db)
    review_item = review_repo.create(
        word_id=review.word_id,
        study_session_id=session_id,
        correct=review.correct
    )
    
    return review_item 