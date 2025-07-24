import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from models import Base, SampleData
from schemas import SampleDataCreate, SampleDataOut, SampleDataUpdate
from crud import (
    create as crud_create,
    get_all as crud_get_all,
    get_by_id as crud_get_by_id,
    update as crud_update,
    delete as crud_delete,
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SampleData CRUD API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=SampleDataOut)
def create_item(item: SampleDataCreate, db: Session = Depends(get_db)):
    return crud_create(db, item)

@app.get("/items/", response_model=List[SampleDataOut])
def read_items(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    first_name: Optional[str] = Query(None, description="Filter by first name, partial match"),
    last_name:  Optional[str] = Query(None, description="Filter by last name, partial match"),
    state:      Optional[str] = Query(None, min_length=2, max_length=2, description="Filter by 2-letter state code"),
    department: Optional[str] = Query(None, description="Filter by department, partial match"),
    city:       Optional[str] = Query(None, description="Filter by city, partial match"),
    email:      Optional[str] = Query(None, description="Filter by email, partial match"),
):
    stmt = select(SampleData)

    if first_name:
        stmt = stmt.where(SampleData.first_name.ilike(f"%{first_name}%"))
    if last_name:
        stmt = stmt.where(SampleData.last_name.ilike(f"%{last_name}%"))
    if state:
        stmt = stmt.where(SampleData.state == state.upper())
    if department:
        stmt = stmt.where(SampleData.department.ilike(f"%{department}%"))
    if city:
        stmt = stmt.where(SampleData.city.ilike(f"%{city}%"))
    if email:
        stmt = stmt.where(SampleData.email.ilike(f"%{email}%"))

    stmt = stmt.offset(skip).limit(limit)
    items = db.scalars(stmt).all()
    return items

@app.get("/items/{item_id}", response_model=SampleDataOut)
def read_item(item_id: int, db: Session = Depends(get_db)):
    obj = crud_get_by_id(db, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj

@app.put("/items/{item_id}", response_model=SampleDataOut)
def update_item(item_id: int, item: SampleDataUpdate, db: Session = Depends(get_db)):
    updated = crud_update(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@app.delete("/items/{item_id}", response_model=SampleDataOut)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted = crud_delete(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted
