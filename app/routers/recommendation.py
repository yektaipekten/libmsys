from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db_session
from .. import models, schemas
from ..recommendation import hybrid_recommendations, filtered_recommendations

router = APIRouter()


@router.get("/{member_id}/recommendations", response_model=List[schemas.Book])
def get_recommendations(member_id: int, db: Session = Depends(get_db_session)):
    recommendations = hybrid_recommendations(member_id, db)
    if recommendations.empty:
        raise HTTPException(
            status_code=404, detail="No recommendations available for this member"
        )
    return recommendations.to_dict("records")


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
