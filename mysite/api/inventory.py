from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import Inventory, Warehouse
from mysite.schemas.inventory_schema import InventoryInputSchema, InventoryOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


inventory_router = APIRouter(prefix='/inventories', tags=['Inventory'])


def _get_warehouse_or_404(db: Session, warehouse_id: int) -> Warehouse:
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(detail='Warehouse not found', status_code=404)
    return warehouse_db


@inventory_router.post('/', response_model=InventoryOutputSchema)
async def create_inventory(inventory: InventoryInputSchema, db: Session = Depends(get_db)):
    _get_warehouse_or_404(db, inventory.warehouse_id)
    if inventory.reserved_quantity > inventory.quantity:
        raise HTTPException(detail='reserved_quantity больше quantity', status_code=400)
    same_db = db.query(Inventory).filter(Inventory.warehouse_id == inventory.warehouse_id,
                                         Inventory.product_id == inventory.product_id).first()
    if same_db:
        raise HTTPException(detail='Inventory already exists', status_code=400)
    inventory_db = Inventory(**inventory.model_dump())
    db.add(inventory_db)
    db.commit()
    db.refresh(inventory_db)
    return inventory_db

@inventory_router.get('/', response_model=List[InventoryOutputSchema])
async def list_inventories(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@inventory_router.get('/{inventory_id}', response_model=InventoryOutputSchema)
async def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(detail='Inventory not found', status_code=404)
    return inventory_db

@inventory_router.put('/{inventory_id}', response_model=dict)
async def update_inventory(inventory_id: int, inventory: InventoryInputSchema, db: Session = Depends(get_db)):
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(detail='Inventory not found', status_code=404)
    _get_warehouse_or_404(db, inventory.warehouse_id)
    if inventory.reserved_quantity > inventory.quantity:
        raise HTTPException(detail='reserved_quantity больше quantity', status_code=400)
    same_db = db.query(Inventory).filter(Inventory.warehouse_id == inventory.warehouse_id,
                                         Inventory.product_id == inventory.product_id,
                                         Inventory.id != inventory_id).first()
    if same_db:
        raise HTTPException(detail='Inventory already exists', status_code=400)
    for inventory_key, inventory_value in inventory.model_dump().items():
        setattr(inventory_db, inventory_key, inventory_value)
    db.commit()
    db.refresh(inventory_db)
    return {'message': 'Inventory был успешно изменен!'}

@inventory_router.delete('/{inventory_id}', response_model=dict)
async def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(detail='Inventory not found', status_code=404)
    db.delete(inventory_db)
    db.commit()
    return {'message': 'Inventory был успешно удален!'}
