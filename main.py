from fastapi import FastAPI
from mysite.admin.setup import setup_admin
from mysite.api import warehouse, inventory, reservation, courier, location, delivery, route, stop, tracking
import uvicorn


delivery_app = FastAPI()

delivery_app.include_router(warehouse.warehouse_router)
delivery_app.include_router(inventory.inventory_router)
delivery_app.include_router(reservation.reservation_router)
delivery_app.include_router(courier.courier_router)
delivery_app.include_router(location.location_router)
delivery_app.include_router(delivery.delivery_router)
delivery_app.include_router(route.route_router)
delivery_app.include_router(stop.stop_router)
delivery_app.include_router(tracking.tracking_router)
setup_admin(delivery_app)


if __name__ == '__main__':
    uvicorn.run(delivery_app, host="127.0.0.1", port=8001)
