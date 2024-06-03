from fastapi import APIRouter, HTTPException, status, Body, Depends
from sqlalchemy.exc import IntegrityError
from fastapi import Depends  
from sqlalchemy.ext.asyncio import AsyncSession  


from db.errors import EntityDoesNotExist
from db.services.cars import CarsService
from schemas.cars import CarsCreate, CarsPatch, CarsRead
from typing import List, Optional


async def get_db() -> AsyncSession:
        async with async_session() as session:  
            yield session  
            await session.commit()
  
  
def get_service(service):  
    def _get_service(session: AsyncSession = Depends(get_db)):  
        return service(session)  
  
    return _get_service

cars_router = APIRouter(tags=["Cars"])

@cars_router.get(
    "/",
    response_model=List[Optional[CarsRead]],
    status_code=status.HTTP_200_OK,
    name="get_cars",
)
async def get_cars(
    service: CarsService = Depends(get_service(CarsService)),
) -> List[Optional[CarsRead]]:
    return await service.list()


@cars_router.post(
    "/",
    response_model=CarsRead,
    status_code=status.HTTP_201_CREATED,
    name="create_car",
)
async def create_car(
    car_create:CarsCreate,
    service: CarsService = Depends(get_service(CarsService)),
) -> CarsRead:
    try:
        return await service.create(car_create=car_create)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig.args[0])
        )


@cars_router.get(
    "/{car_id}",
    response_model=CarsRead,
    status_code=status.HTTP_200_OK,
    name="get_car",
)
async def get_car(
    car_id: int,
    service: CarsService = Depends(get_service(CarsService)),
) -> CarsRead:
    try:
        return await service.get(car_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found!"
        )


@cars_router.put(
    "/{car_id}",
    response_model=CarsRead,
    status_code=status.HTTP_200_OK,
    name="patch_car",
)
async def patch_car(
    car_id: int,
    cars_patch: CarsPatch,
    service: CarsService = Depends(get_service(CarsService)),
) -> CarsRead:
    try:
        return await service.patch(car_id=car_id, cars_patch=cars_patch)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig.args[0])
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found!"
        )


@cars_router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_car",
)
async def delete_car(
    car_id: int,
    service: CarsService = Depends(get_service(CarsService)),
) -> None:
    try:
        return await service.delete(car_id=car_id)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig.args[0])
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found!"
        )
