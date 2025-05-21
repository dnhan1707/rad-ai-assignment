from fastapi import FastAPI


app = FastAPI(
    title="Food Facilities API"
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Jack's assignment on Food Facilities API"
    }


