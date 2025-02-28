from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from repositories import WordRepository, GroupRepository
import schemas
from schemas import GroupResponse, PaginatedResponse
from utils.rate_limiter import RateLimiter

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=60)

@router.get("/groups", response_model=PaginatedResponse[GroupResponse])
async def get_groups(
    request: Request,
    page: Optional[int] = Query(1, ge=1),
    sort_by: Optional[str] = Query('name', regex='^(name|words_count)$'),
    order: Optional[str] = Query('asc', regex='^(asc|desc)$'),
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    group_repo = GroupRepository(db)
    groups, total = group_repo.get_paginated(
        page=page,
        sort_by=sort_by,
        order=order
    )
    
    return {
        "items": groups,
        "total": total,
        "page": page,
        "has_more": total > page * 10  # Assuming 10 items per page
    }

@router.get("/groups/{group_id}", response_model=GroupResponse)
async def get_group(
    request: Request,
    group_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    group_repo = GroupRepository(db)
    group = group_repo.get_by_id(group_id)
    
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
        
    return group 


@router.get("/groups/{group_id}/words")
async def get_group_words(
    request: Request,
    group_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limiter)
):
    group_repo = GroupRepository(db)
    group = group_repo.get_by_id(group_id)
    
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
        
    word_repo = WordRepository(db)
    words = word_repo.get_by_group_paginated(group_id, per_page=100)
    
    return words[0]