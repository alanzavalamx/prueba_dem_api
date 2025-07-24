from sqlalchemy import select, update as sa_update, delete as sa_delete
from sqlalchemy.orm import Session
from models import SampleData
from schemas import SampleDataCreate, SampleDataUpdate

def get_all(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(SampleData).offset(skip).limit(limit)
    return db.scalars(stmt).all()

def get_by_id(db: Session, item_id: int):
    return db.get(SampleData, item_id)

def get_by_email(db: Session, email: str):
    return db.scalars(select(SampleData).where(SampleData.email == email)).first()

def create(db: Session, item: SampleDataCreate):
    db_obj = SampleData(**item.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, item_id: int, item: SampleDataUpdate):
    stmt = sa_update(SampleData).where(SampleData.id == item_id).values(**item.model_dump(exclude_unset=True)).returning(SampleData)
    result = db.execute(stmt)
    db.commit()
    return result.scalar_one_or_none()

def delete(db: Session, item_id: int):
    stmt = sa_delete(SampleData).where(SampleData.id == item_id).returning(SampleData)
    result = db.execute(stmt)
    db.commit()
    return result.scalar_one_or_none()
