from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import InventoryReservation, Inventory
from mysite.schemas.reservation_schema import ReservationInputSchema, ReservationOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


reservation_router = APIRouter(prefix='/reservations', tags=['InventoryReservation'])


def _get_inventory_or_404(db: Session, inventory_id: int) -> Inventory:
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(detail='Inventory not found', status_code=404)
    return inventory_db


@reservation_router.post('/', response_model=ReservationOutputSchema)
async def create_reservation(reservation: ReservationInputSchema, db: Session = Depends(get_db)):
    _get_inventory_or_404(db, reservation.inventory_id)
    reservation_db = InventoryReservation(**reservation.model_dump())
    db.add(reservation_db)
    db.commit()
    db.refresh(reservation_db)
    return reservation_db

@reservation_router.get('/', response_model=List[ReservationOutputSchema])
async def list_reservations(db: Session = Depends(get_db)):
    return db.query(InventoryReservation).all()

@reservation_router.get('/{reservation_id}', response_model=ReservationOutputSchema)
async def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_db = db.query(InventoryReservation).filter(InventoryReservation.id == reservation_id).first()
    if not reservation_db:
        raise HTTPException(detail='Reservation not found', status_code=404)
    return reservation_db

@reservation_router.put('/{reservation_id}', response_model=dict)
async def update_reservation(reservation_id: int, reservation: ReservationInputSchema, db: Session = Depends(get_db)):
    reservation_db = db.query(InventoryReservation).filter(InventoryReservation.id == reservation_id).first()
    if not reservation_db:
        raise HTTPException(detail='Reservation not found', status_code=404)
    _get_inventory_or_404(db, reservation.inventory_id)
    for reservation_key, reservation_value in reservation.model_dump().items():
        setattr(reservation_db, reservation_key, reservation_value)
    db.commit()
    db.refresh(reservation_db)
    return {'message': 'Reservation был успешно изменен!'}

@reservation_router.delete('/{reservation_id}', response_model=dict)
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_db = db.query(InventoryReservation).filter(InventoryReservation.id == reservation_id).first()
    if not reservation_db:
        raise HTTPException(detail='Reservation not found', status_code=404)
    db.delete(reservation_db)
    db.commit()
    return {'message': 'Reservation был успешно удален!'}
