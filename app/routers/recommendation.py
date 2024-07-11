from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db_session
from .. import models, schemas
from ..recommendation import (
    hybrid_recommendations,
    filtered_recommendations,
    member_recommendations,
)
from . import recommendation

router = APIRouter()


@router.get("/filtered", response_model=List[schemas.Book])
def get_filtered_recommendations(
    category: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    db: Session = Depends(get_db_session),
):
    try:
        recommendations = filtered_recommendations(category, language, title, db)
        if not recommendations:
            raise HTTPException(
                status_code=404,
                detail="No recommendations available based on the given criteria",
            )
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recommendations/member/{member_id}")
def get_member_recommendations(member_id: int, db: Session = Depends(get_db_session)):
    try:
        recommendations = recommendation.member_recommendations(member_id, db)
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
