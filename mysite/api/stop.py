from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import RouteStop, Route, Delivery
from mysite.schemas.stop_schema import StopInputSchema, StopOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


stop_router = APIRouter(prefix='/stops', tags=['RouteStop'])


def _get_route_or_404(db: Session, route_id: int) -> Route:
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(detail='Route not found', status_code=404)
    return route_db


def _get_delivery_or_404(db: Session, delivery_id: int) -> Delivery:
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(detail='Delivery not found', status_code=404)
    return delivery_db


@stop_router.post('/', response_model=StopOutputSchema)
async def create_stop(stop: StopInputSchema, db: Session = Depends(get_db)):
    _get_route_or_404(db, stop.route_id)
    _get_delivery_or_404(db, stop.delivery_id)
    stop_db = RouteStop(**stop.model_dump())
    db.add(stop_db)
    db.commit()
    db.refresh(stop_db)
    return stop_db

@stop_router.get('/', response_model=List[StopOutputSchema])
async def list_stops(db: Session = Depends(get_db)):
    return db.query(RouteStop).all()

@stop_router.get('/{stop_id}', response_model=StopOutputSchema)
async def get_stop(stop_id: int, db: Session = Depends(get_db)):
    stop_db = db.query(RouteStop).filter(RouteStop.id == stop_id).first()
    if not stop_db:
        raise HTTPException(detail='Stop not found', status_code=404)
    return stop_db

@stop_router.put('/{stop_id}', response_model=dict)
async def update_stop(stop_id: int, stop: StopInputSchema, db: Session = Depends(get_db)):
    stop_db = db.query(RouteStop).filter(RouteStop.id == stop_id).first()
    if not stop_db:
        raise HTTPException(detail='Stop not found', status_code=404)
    _get_route_or_404(db, stop.route_id)
    _get_delivery_or_404(db, stop.delivery_id)
    for stop_key, stop_value in stop.model_dump().items():
        setattr(stop_db, stop_key, stop_value)
    db.commit()
    db.refresh(stop_db)
    return {'message': 'Stop был успешно изменен!'}

@stop_router.delete('/{stop_id}', response_model=dict)
async def delete_stop(stop_id: int, db: Session = Depends(get_db)):
    stop_db = db.query(RouteStop).filter(RouteStop.id == stop_id).first()
    if not stop_db:
        raise HTTPException(detail='Stop not found', status_code=404)
    db.delete(stop_db)
    db.commit()
    return {'message': 'Stop был успешно удален!'}
