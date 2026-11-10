from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import Route, Courier
from mysite.schemas.route_schema import RouteInputSchema, RouteOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


route_router = APIRouter(prefix='/routes', tags=['Route'])


def _get_courier_or_404(db: Session, courier_id: int) -> Courier:
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='Courier not found', status_code=404)
    return courier_db


@route_router.post('/', response_model=RouteOutputSchema)
async def create_route(route: RouteInputSchema, db: Session = Depends(get_db)):
    _get_courier_or_404(db, route.courier_id)
    route_db = Route(**route.model_dump())
    db.add(route_db)
    db.commit()
    db.refresh(route_db)
    return route_db

@route_router.get('/', response_model=List[RouteOutputSchema])
async def list_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()

@route_router.get('/{route_id}', response_model=RouteOutputSchema)
async def get_route(route_id: int, db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(detail='Route not found', status_code=404)
    return route_db

@route_router.put('/{route_id}', response_model=dict)
async def update_route(route_id: int, route: RouteInputSchema, db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(detail='Route not found', status_code=404)
    _get_courier_or_404(db, route.courier_id)
    for route_key, route_value in route.model_dump().items():
        setattr(route_db, route_key, route_value)
    db.commit()
    db.refresh(route_db)
    return {'message': 'Route был успешно изменен!'}

@route_router.delete('/{route_id}', response_model=dict)
async def delete_route(route_id: int, db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(detail='Route not found', status_code=404)
    db.delete(route_db)
    db.commit()
    return {'message': 'Route был успешно удален!'}
