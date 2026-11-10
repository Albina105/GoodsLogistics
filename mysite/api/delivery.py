from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import Delivery, Warehouse, Courier
from mysite.schemas.delivery_schema import DeliveryInputSchema, DeliveryOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


delivery_router = APIRouter(prefix='/deliveries', tags=['Delivery'])


def _get_warehouse_or_404(db: Session, warehouse_id: int) -> Warehouse:
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(detail='Warehouse not found', status_code=404)
    return warehouse_db


def _get_courier_or_404(db: Session, courier_id: int) -> Courier:
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='Courier not found', status_code=404)
    return courier_db


@delivery_router.post('/', response_model=DeliveryOutputSchema)
async def create_delivery(delivery: DeliveryInputSchema, db: Session = Depends(get_db)):
    _get_warehouse_or_404(db, delivery.warehouse_id)
    if delivery.courier_id is not None:
        _get_courier_or_404(db, delivery.courier_id)
    if db.query(Delivery).filter(Delivery.tracking_code == delivery.tracking_code).first():
        raise HTTPException(detail='Tracking code already exists', status_code=400)
    delivery_db = Delivery(**delivery.model_dump())
    db.add(delivery_db)
    db.commit()
    db.refresh(delivery_db)
    return delivery_db

@delivery_router.get('/', response_model=List[DeliveryOutputSchema])
async def list_deliveries(db: Session = Depends(get_db)):
    return db.query(Delivery).all()

@delivery_router.get('/{delivery_id}', response_model=DeliveryOutputSchema)
async def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(detail='Delivery not found', status_code=404)
    return delivery_db

@delivery_router.put('/{delivery_id}', response_model=dict)
async def update_delivery(delivery_id: int, delivery: DeliveryInputSchema, db: Session = Depends(get_db)):
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(detail='Delivery not found', status_code=404)
    _get_warehouse_or_404(db, delivery.warehouse_id)
    if delivery.courier_id is not None:
        _get_courier_or_404(db, delivery.courier_id)
    same_db = db.query(Delivery).filter(Delivery.tracking_code == delivery.tracking_code,
                                        Delivery.id != delivery_id).first()
    if same_db:
        raise HTTPException(detail='Tracking code already exists', status_code=400)
    for delivery_key, delivery_value in delivery.model_dump().items():
        setattr(delivery_db, delivery_key, delivery_value)
    db.commit()
    db.refresh(delivery_db)
    return {'message': 'Delivery был успешно изменен!'}

@delivery_router.delete('/{delivery_id}', response_model=dict)
async def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(detail='Delivery not found', status_code=404)
    db.delete(delivery_db)
    db.commit()
    return {'message': 'Delivery был успешно удален!'}
