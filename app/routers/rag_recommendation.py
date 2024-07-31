from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db_session
from app.rag import get_recommendations_for_member, get_recommendations_based_on_prompt
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/recommendations/member/{member_id}")
async def recommend_books_for_member(
    member_id: int, db: Session = Depends(get_db_session)
):
    try:
        logger.info(f"Member ID: {member_id} get recommendation for member")
        recommendations = get_recommendations_for_member(member_id, db)
        logger.info(f"Recommendations: {recommendations}")
        return {"recommendations": recommendations}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
