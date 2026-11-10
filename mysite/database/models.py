from .db import Base
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, Optional
from enum import Enum as PyEnum


class WarehouseStatus(str, PyEnum):
    active = 'active'
    inactive = 'inactive'
    maintenance = 'maintenance'


class ReservationStatus(str, PyEnum):
    active = 'active'
    committed = 'committed'
    released = 'released'
    expired = 'expired'


class TransportType(str, PyEnum):
    walking = 'walking'
    bicycle = 'bicycle'
    motorcycle = 'motorcycle'
    car = 'car'


class CourierStatus(str, PyEnum):
    offline = 'offline'
    available = 'available'
    busy = 'busy'
    suspended = 'suspended'


class DeliveryStatus(str, PyEnum):
    created = 'created'
    assigned = 'assigned'
    picked_up = 'picked_up'
    on_the_way = 'on_the_way'
    delivered = 'delivered'
    cancelled = 'cancelled'


class RouteStatus(str, PyEnum):
    planned = 'planned'
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'


class StopType(str, PyEnum):
    pickup = 'pickup'
    dropoff = 'dropoff'


class StopStatus(str, PyEnum):
    pending = 'pending'
    arrived = 'arrived'
    completed = 'completed'
    skipped = 'skipped'


class Warehouse(Base):
    __tablename__ = 'warehouse'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    city_id: Mapped[int] = mapped_column(Integer)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    street: Mapped[str] = mapped_column(String(128))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    capacity: Mapped[int] = mapped_column(Integer)
    status: Mapped[WarehouseStatus] = mapped_column(Enum(WarehouseStatus),
                                                    default=WarehouseStatus.active)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    warehouse_inventories: Mapped[List['Inventory']] = relationship(back_populates='warehouse',
                                                                    cascade='all, delete-orphan')
    warehouse_couriers: Mapped[List['Courier']] = relationship(back_populates='warehouse',
                                                               cascade='all, delete-orphan')
    warehouse_deliveries: Mapped[List['Delivery']] = relationship(back_populates='warehouse',
                                                                  cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.code}, {self.name}'


class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouse.id'))
    warehouse: Mapped[Warehouse] = relationship(back_populates='warehouse_inventories')
    product_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now,
                                                 onupdate=datetime.now)
    inventory_reservations: Mapped[List['InventoryReservation']] = relationship(
        back_populates='inventory', cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.warehouse_id}, {self.product_id}, {self.quantity}'


class InventoryReservation(Base):
    __tablename__ = 'inventory_reservation'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer)
    inventory_id: Mapped[int] = mapped_column(ForeignKey('inventory.id'))
    inventory: Mapped[Inventory] = relationship(back_populates='inventory_reservations')
    quantity: Mapped[int] = mapped_column(Integer)
    status: Mapped[ReservationStatus] = mapped_column(Enum(ReservationStatus),
                                                      default=ReservationStatus.active)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __str__(self):
        return f'{self.order_id}, {self.quantity}, {self.status}'


class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouse.id'))
    warehouse: Mapped[Warehouse] = relationship(back_populates='warehouse_couriers')
    transport_type: Mapped[TransportType] = mapped_column(Enum(TransportType))
    status: Mapped[CourierStatus] = mapped_column(Enum(CourierStatus),
                                                  default=CourierStatus.offline)
    max_active_orders: Mapped[int] = mapped_column(Integer, default=3)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    courier_locations: Mapped[List['CourierLocation']] = relationship(back_populates='courier',
                                                                      cascade='all, delete-orphan')
    courier_deliveries: Mapped[List['Delivery']] = relationship(back_populates='courier')
    courier_routes: Mapped[List['Route']] = relationship(back_populates='courier',
                                                         cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.user_id}, {self.transport_type}'


class CourierLocation(Base):
    __tablename__ = 'courier_location'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'))
    courier: Mapped[Courier] = relationship(back_populates='courier_locations')
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __str__(self):
        return f'{self.courier_id}, {self.latitude}, {self.longitude}'


class Delivery(Base):
    __tablename__ = 'delivery'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouse.id'))
    warehouse: Mapped[Warehouse] = relationship(back_populates='warehouse_deliveries')
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey('courier.id'), nullable=True)
    courier: Mapped[Optional['Courier']] = relationship(back_populates='courier_deliveries')
    tracking_code: Mapped[str] = mapped_column(String(32), unique=True)
    status: Mapped[DeliveryStatus] = mapped_column(Enum(DeliveryStatus),
                                                   default=DeliveryStatus.created)
    destination_address: Mapped[str] = mapped_column(String(256))
    destination_latitude: Mapped[float] = mapped_column(Float)
    destination_longitude: Mapped[float] = mapped_column(Float)
    estimated_delivery_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    delivery_stops: Mapped[List['RouteStop']] = relationship(back_populates='delivery',
                                                             cascade='all, delete-orphan')
    delivery_events: Mapped[List['TrackingEvent']] = relationship(back_populates='delivery',
                                                                  cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.tracking_code}, {self.status}'


class Route(Base):
    __tablename__ = 'route'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'))
    courier: Mapped[Courier] = relationship(back_populates='courier_routes')
    status: Mapped[RouteStatus] = mapped_column(Enum(RouteStatus), default=RouteStatus.planned)
    total_distance_km: Mapped[float] = mapped_column(Float, default=0)
    estimated_duration_min: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    route_stops: Mapped[List['RouteStop']] = relationship(back_populates='route',
                                                          cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.id}, {self.status}'


class RouteStop(Base):
    __tablename__ = 'route_stop'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey('route.id'))
    route: Mapped[Route] = relationship(back_populates='route_stops')
    delivery_id: Mapped[int] = mapped_column(ForeignKey('delivery.id'))
    delivery: Mapped[Delivery] = relationship(back_populates='delivery_stops')
    stop_type: Mapped[StopType] = mapped_column(Enum(StopType))
    sequence: Mapped[int] = mapped_column(Integer)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    status: Mapped[StopStatus] = mapped_column(Enum(StopStatus), default=StopStatus.pending)
    arrived_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __str__(self):
        return f'{self.route_id}, {self.sequence}, {self.stop_type}'


class TrackingEvent(Base):
    __tablename__ = 'tracking_event'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey('delivery.id'))
    delivery: Mapped[Delivery] = relationship(back_populates='delivery_events')
    status: Mapped[DeliveryStatus] = mapped_column(Enum(DeliveryStatus))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __str__(self):
        return f'{self.delivery_id}, {self.status}'
