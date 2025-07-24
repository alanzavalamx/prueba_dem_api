# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import csv
import os

from main import app, get_db
from models import Base
from schemas import SampleDataCreate
from crud import create as crud_create

# Configuración de PostgreSQL para los tests de la API
TEST_DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"
engine = create_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=Session, expire_on_commit=False)

# Crear esquema en memoria
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_read_initial_data():
    resp = client.get("/items/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 100


def test_full_crud_flow():
    # CREATE
    payload = {
        "first_name": "Juan",
        "last_name": "Perez",
        "state": "NL",
        "email": "juan.perez@example.com"
    }
    res = client.post("/items/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["first_name"] == "Juan"
    item_id = data["id"]

    # READ ONE
    res = client.get(f"/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["email"] == "juan.perez@example.com"

    # UPDATE
    update_payload = {"email": "juan.updated@example.com"}
    res = client.put(f"/items/{item_id}", json=update_payload)
    assert res.status_code == 200
    assert res.json()["email"] == "juan.updated@example.com"

    # DELETE
    res = client.delete(f"/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["id"] == item_id

    # READ NOT FOUND
    res = client.get(f"/items/{item_id}")
    assert res.status_code == 404
