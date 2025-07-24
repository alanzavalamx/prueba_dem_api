# api/schemas.py

from typing import Optional, Annotated
from pydantic import BaseModel, Field, constr

class SampleDataBase(BaseModel):
    first_name:  Annotated[str, constr(min_length=1, max_length=100)]
    last_name:   Annotated[str, constr(min_length=1, max_length=100)]
    company_name: Optional[str] = None
    address:      Optional[str] = None
    city:         Optional[str] = None

    state:        str = Field(
        ..., 
        min_length=2, 
        max_length=2, 
        pattern=r'^[A-Za-z]{2}$',
        description="Código de estado: dos letras"
    )

    zip:          Optional[str] = None
    phone1:       Optional[str] = None
    phone2:       Optional[str] = None
    email:        Optional[str] = None
    department:   Optional[str] = None

class SampleDataCreate(SampleDataBase):
    pass

class SampleDataUpdate(BaseModel):
    # Permitimos campos opcionales al actualizar
    first_name:  Optional[Annotated[str, constr(min_length=1, max_length=100)]] = None
    last_name:   Optional[Annotated[str, constr(min_length=1, max_length=100)]] = None
    company_name: Optional[str] = None
    address:      Optional[str] = None
    city:         Optional[str] = None
    state:        Optional[str] = Field(
        None,
        min_length=2, 
        max_length=2, 
        pattern=r'^[A-Za-z]{2}$',
        description="Código de estado: dos letras"
    )
    zip:          Optional[str] = None
    phone1:       Optional[str] = None
    phone2:       Optional[str] = None
    email:        Optional[str] = None
    department:   Optional[str] = None

class SampleDataOut(SampleDataBase):
    id: int

    model_config = {
        "from_attributes": True
    }
