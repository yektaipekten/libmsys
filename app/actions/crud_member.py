from sqlalchemy.orm import Session
from .. import models, schemas

# Member CRUD Operations


def create_member(db: Session, member: schemas.MemberCreate, library_id: int):
    member_data = member.dict()
    member_data.pop("library_id", None)
    db_member = models.Member(**member_data, library_id=library_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()


def show_member_info(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()


def remove_member(db: Session, member_id: int):
    db_member = (
        db.query(models.Member).filter(models.Member.member_id == member_id).first()
    )
    if db_member:
        db.delete(db_member)
        db.commit()
    return db_member
