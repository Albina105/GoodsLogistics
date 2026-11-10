from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import CourierLocation, Courier
from mysite.schemas.location_schema import LocationInputSchema, LocationOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


location_router = APIRouter(prefix='/locations', tags=['CourierLocation'])


def _get_courier_or_404(db: Session, courier_id: int) -> Courier:
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='Courier not found', status_code=404)
    return courier_db


@location_router.post('/', response_model=LocationOutputSchema)
async def create_location(location: LocationInputSchema, db: Session = Depends(get_db)):
    _get_courier_or_404(db, location.courier_id)
    location_db = CourierLocation(**location.model_dump())
    db.add(location_db)
    db.commit()
    db.refresh(location_db)
    return location_db

@location_router.get('/', response_model=List[LocationOutputSchema])
async def list_locations(db: Session = Depends(get_db)):
    return db.query(CourierLocation).all()

@location_router.get('/{location_id}', response_model=LocationOutputSchema)
async def get_location(location_id: int, db: Session = Depends(get_db)):
    location_db = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location_db:
        raise HTTPException(detail='Location not found', status_code=404)
    return location_db

@location_router.put('/{location_id}', response_model=dict)
async def update_location(location_id: int, location: LocationInputSchema, db: Session = Depends(get_db)):
    location_db = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location_db:
        raise HTTPException(detail='Location not found', status_code=404)
    _get_courier_or_404(db, location.courier_id)
    for location_key, location_value in location.model_dump().items():
        setattr(location_db, location_key, location_value)
    db.commit()
    db.refresh(location_db)
    return {'message': 'Location был успешно изменен!'}

@location_router.delete('/{location_id}', response_model=dict)
async def delete_location(location_id: int, db: Session = Depends(get_db)):
    location_db = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location_db:
        raise HTTPException(detail='Location not found', status_code=404)
    db.delete(location_db)
    db.commit()
    return {'message': 'Location был успешно удален!'}
