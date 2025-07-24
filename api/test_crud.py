# tests/test_crud.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, SampleData
from crud import create, get_all, get_by_id, update, delete, get_by_email
from schemas import SampleDataCreate, SampleDataUpdate


@pytest.fixture(scope="module")
def engine():
    # Usamos PostgreSQL para pruebas unitarias
    engine = create_engine(
        "postgresql://postgres:postgres@db:5432/postgres", future=True)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db(engine):
    SessionLocal = sessionmaker(
        bind=engine, class_=Session, expire_on_commit=False)
    session = SessionLocal()
    yield session
    session.close()


def test_create_and_get(db):
    payload = SampleDataCreate(
        first_name="Alan",
        last_name="Zavala",
        state="NL",
        email="alan.zavala@example.com"
    )
    created = create(db, payload)
    assert created.email == "alan.zavala@example.com"

    fetched = get_by_id(db, created.id)
    assert fetched is not None
    assert fetched.first_name == "Alan"


def test_get_all(db):
    items = get_all(db)
    assert len(items) != 1


def test_update(db):
    update_data = SampleDataUpdate(email="alan.updated@example.com")
    fetched = get_by_email(db, "alan.zavala@example.com")
    updated = update(db, fetched.id, update_data)
    assert updated is not None
    assert updated.email == "alan.updated@example.com"


def test_delete(db):
    fetched = get_by_email(db, "alan.updated@example.com")
    assert fetched is not None, "No se encontró el registro a borrar"

    deleted = delete(db, fetched.id)
    assert deleted is not None, "La función delete no devolvió el objeto borrado"

    again = get_by_id(db, fetched.id)
    assert again is not None, "El registro no fue eliminado correctamente"