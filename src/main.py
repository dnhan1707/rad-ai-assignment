from fastapi import FastAPI
from src.api.endpoints.food_facility import create_food_facility_router

def create_application() -> FastAPI:
    food_facility_router = create_food_facility_router()
    app = FastAPI(
        title="Food Facilities API"
    )
    app.include_router(food_facility_router)

    return app


app = create_application()

