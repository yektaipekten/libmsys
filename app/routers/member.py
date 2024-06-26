from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db_session

router = APIRouter(
    prefix="/members",
    tags=["members"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db_session)):
    return crud.create_member(db, member)


@router.get("/{member_id}", response_model=schemas.Member)
def read_member(member_id: int, db: Session = Depends(get_db_session)):
    db_member = crud.get_member(db, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.get("/", response_model=list[schemas.Member])
def read_members(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    members = crud.get_members(db, skip=skip, limit=limit)
    return members


@router.put("/{member_id}", response_model=schemas.Member)
def update_member(
    member_id: int, member: schemas.MemberUpdate, db: Session = Depends(get_db_session)
):
    db_member = crud.update_member(db, member_id, member)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.delete("/{member_id}", response_model=schemas.Member)
def delete_member(member_id: int, db: Session = Depends(get_db_session)):
    db_member = crud.delete_member(db, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member
