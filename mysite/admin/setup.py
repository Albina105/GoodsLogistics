from .views import (WarehouseAdmin, InventoryAdmin, InventoryReservationAdmin, CourierAdmin,
                    CourierLocationAdmin, DeliveryAdmin, RouteAdmin, RouteStopAdmin,
                    TrackingEventAdmin)

from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine


def setup_admin(delivery_app: FastAPI):
    admin = Admin(delivery_app, engine)
    admin.add_view(WarehouseAdmin)
    admin.add_view(InventoryAdmin)
    admin.add_view(InventoryReservationAdmin)
    admin.add_view(CourierAdmin)
    admin.add_view(CourierLocationAdmin)
    admin.add_view(DeliveryAdmin)
    admin.add_view(RouteAdmin)
    admin.add_view(RouteStopAdmin)
    admin.add_view(TrackingEventAdmin)
