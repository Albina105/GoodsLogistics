from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import Warehouse
from mysite.schemas.warehouse_schema import WarehouseInputSchema, WarehouseOutputSchema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


warehouse_router = APIRouter(prefix='/warehouses', tags=['Warehouse'])


@warehouse_router.post('/', response_model=WarehouseOutputSchema)
async def create_warehouse(warehouse: WarehouseInputSchema, db: Session = Depends(get_db)):
    if db.query(Warehouse).filter(Warehouse.code == warehouse.code).first():
        raise HTTPException(detail='Warehouse code already exists', status_code=400)
    warehouse_db = Warehouse(**warehouse.model_dump())
    db.add(warehouse_db)
    db.commit()
    db.refresh(warehouse_db)
    return warehouse_db

@warehouse_router.get('/', response_model=List[WarehouseOutputSchema])
async def list_warehouses(db: Session = Depends(get_db)):
    return db.query(Warehouse).all()

@warehouse_router.get('/{warehouse_id}', response_model=WarehouseOutputSchema)
async def get_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(detail='Warehouse not found', status_code=404)
    return warehouse_db

@warehouse_router.put('/{warehouse_id}', response_model=dict)
async def update_warehouse(warehouse_id: int, warehouse: WarehouseInputSchema, db: Session = Depends(get_db)):
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(detail='Warehouse not found', status_code=404)
    same_db = db.query(Warehouse).filter(Warehouse.code == warehouse.code,
                                         Warehouse.id != warehouse_id).first()
    if same_db:
        raise HTTPException(detail='Warehouse code already exists', status_code=400)
    for warehouse_key, warehouse_value in warehouse.model_dump().items():
        setattr(warehouse_db, warehouse_key, warehouse_value)
    db.commit()
    db.refresh(warehouse_db)
    return {'message': 'Warehouse был успешно изменен!'}

@warehouse_router.delete('/{warehouse_id}', response_model=dict)
async def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(detail='Warehouse not found', status_code=404)
    db.delete(warehouse_db)
    db.commit()
    return {'message': 'Warehouse был успешно удален!'}
