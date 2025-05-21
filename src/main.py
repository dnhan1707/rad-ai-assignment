from fastapi import FastAPI
from src.api.endpoints.food_facility import router

app = FastAPI(
    title="Food Facilities API"
)
app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Jack's assignment on Food Facilities API"
    }


