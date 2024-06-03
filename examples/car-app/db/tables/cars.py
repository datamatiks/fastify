from sqlmodel import SQLModel, UniqueConstraint, Field
from db.tables.base_class import DatesModel, IDModel
from typing import Optional

class CarsBase(SQLModel):
    __table_args__ = (
        UniqueConstraint("car_name", name="cars_car_name_key"),
    )
    car_name: str
    created_by: str
    updated_by: str


class Cars(CarsBase, IDModel, DatesModel, table=True):
    __tablename__ = "cars"
