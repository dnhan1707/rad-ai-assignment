from fastapi import FastAPI
from src.api.endpoints.logging import router

app = FastAPI(
    title="Food Facilities API"
)
app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Jack's assignment on Food Facilities API"
    }


