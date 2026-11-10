from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import Courier, Warehouse
from mysite.schemas.courier_schema import CourierInputSchema, CourierOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


courier_router = APIRouter(prefix='/couriers', tags=['Courier'])


def _get_warehouse_or_404(db: Session, warehouse_id: int) -> Warehouse:
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(detail='Warehouse not found', status_code=404)
    return warehouse_db


@courier_router.post('/', response_model=CourierOutputSchema)
async def create_courier(courier: CourierInputSchema, db: Session = Depends(get_db)):
    _get_warehouse_or_404(db, courier.warehouse_id)
    if db.query(Courier).filter(Courier.user_id == courier.user_id).first():
        raise HTTPException(detail='Courier already exists', status_code=400)
    courier_db = Courier(**courier.model_dump())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db

@courier_router.get('/', response_model=List[CourierOutputSchema])
async def list_couriers(db: Session = Depends(get_db)):
    return db.query(Courier).all()

@courier_router.get('/{courier_id}', response_model=CourierOutputSchema)
async def get_courier(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='Courier not found', status_code=404)
    return courier_db

@courier_router.put('/{courier_id}', response_model=dict)
async def update_courier(courier_id: int, courier: CourierInputSchema, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='Courier not found', status_code=404)
    _get_warehouse_or_404(db, courier.warehouse_id)
    same_db = db.query(Courier).filter(Courier.user_id == courier.user_id,
                                       Courier.id != courier_id).first()
    if same_db:
        raise HTTPException(detail='Courier already exists', status_code=400)
    for courier_key, courier_value in courier.model_dump().items():
        setattr(courier_db, courier_key, courier_value)
    db.commit()
    db.refresh(courier_db)
    return {'message': 'Courier был успешно изменен!'}

@courier_router.delete('/{courier_id}', response_model=dict)
async def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='Courier not found', status_code=404)
    db.delete(courier_db)
    db.commit()
    return {'message': 'Courier был успешно удален!'}
