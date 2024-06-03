from db.tables.cars import CarsBase, Cars
from sqlmodel import SQLModel, Field
from sqlalchemy.sql import text
from typing import Optional

class CarsCreate(CarsBase):
    ...

class CarsRead(Cars):
    ...

class CarsPatch(SQLModel):
    car_name: Optional[str] = None
    updated_by: str = None
