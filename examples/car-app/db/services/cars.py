from sqlmodel.ext.asyncio.session import AsyncSession
from db.tables.cars import Cars
from db.errors import EntityDoesNotExist
from schemas.cars import CarsCreate, CarsPatch, CarsRead
from sqlmodel import select
from typing import List, Optional

class CarsService:
    def __init__(self, session:AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, car_id: int):
        statement = (
            select(Cars)
            .where(Cars.id == car_id)
        )
        results = await self.session.exec(statement)
        return results.first()

    async def create(self, car_create: CarsCreate) -> CarsRead:
        db_transaction = Cars.from_orm(car_create)
        self.session.add(db_transaction)
        await self.session.commit()
        await self.session.refresh(db_transaction)

        return CarsRead(**db_transaction.dict())
    
    async def list(self) -> List[CarsRead]:
        results = await self.session.execute(
            select(Cars)
        )

        return [
            CarsRead(**car.dict())
            for car in results.scalars()
        ]
    
    async def get(self, car_id: int) -> Optional[CarsRead]:
        db_transaction = await self._get_instance(car_id)
        if db_transaction is None:
            raise EntityDoesNotExist
        
        return CarsRead(**db_transaction.dict())
    
    async def patch(self, car_id: int, cars_patch: CarsPatch) -> Optional[CarsRead]:
        db_transaction = await self._get_instance(car_id)

        if db_transaction is None:
            raise EntityDoesNotExist
        
        transaction_data = cars_patch.dict(exclude_none=True)
        for key, value in transaction_data.items():
            setattr(db_transaction, key, value)
        self.session.add(db_transaction)
        await self.session.commit()
        await self.session.refresh(db_transaction)

        return CarsRead(**db_transaction.dict())
    
    async def delete(self, car_id: int) -> None:
        car = await self._get_instance(car_id)

        if car is None:
            raise EntityDoesNotExist

        await self.session.delete(car)
        await self.session.commit()
        return {"ok": True}
