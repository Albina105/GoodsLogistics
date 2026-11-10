from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import TrackingEvent, Delivery
from mysite.schemas.tracking_schema import TrackingInputSchema, TrackingOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tracking_router = APIRouter(prefix='/tracking', tags=['TrackingEvent'])


def _get_delivery_or_404(db: Session, delivery_id: int) -> Delivery:
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(detail='Delivery not found', status_code=404)
    return delivery_db


@tracking_router.post('/', response_model=TrackingOutputSchema)
async def create_tracking(tracking: TrackingInputSchema, db: Session = Depends(get_db)):
    _get_delivery_or_404(db, tracking.delivery_id)
    tracking_db = TrackingEvent(**tracking.model_dump())
    db.add(tracking_db)
    db.commit()
    db.refresh(tracking_db)
    return tracking_db

@tracking_router.get('/', response_model=List[TrackingOutputSchema])
async def list_tracking(db: Session = Depends(get_db)):
    return db.query(TrackingEvent).all()

@tracking_router.get('/{tracking_id}', response_model=TrackingOutputSchema)
async def get_tracking(tracking_id: int, db: Session = Depends(get_db)):
    tracking_db = db.query(TrackingEvent).filter(TrackingEvent.id == tracking_id).first()
    if not tracking_db:
        raise HTTPException(detail='Tracking not found', status_code=404)
    return tracking_db

@tracking_router.put('/{tracking_id}', response_model=dict)
async def update_tracking(tracking_id: int, tracking: TrackingInputSchema, db: Session = Depends(get_db)):
    tracking_db = db.query(TrackingEvent).filter(TrackingEvent.id == tracking_id).first()
    if not tracking_db:
        raise HTTPException(detail='Tracking not found', status_code=404)
    _get_delivery_or_404(db, tracking.delivery_id)
    for tracking_key, tracking_value in tracking.model_dump().items():
        setattr(tracking_db, tracking_key, tracking_value)
    db.commit()
    db.refresh(tracking_db)
    return {'message': 'Tracking был успешно изменен!'}

@tracking_router.delete('/{tracking_id}', response_model=dict)
async def delete_tracking(tracking_id: int, db: Session = Depends(get_db)):
    tracking_db = db.query(TrackingEvent).filter(TrackingEvent.id == tracking_id).first()
    if not tracking_db:
        raise HTTPException(detail='Tracking not found', status_code=404)
    db.delete(tracking_db)
    db.commit()
    return {'message': 'Tracking был успешно удален!'}
