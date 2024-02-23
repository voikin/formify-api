from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from routers.auth_router import router as auth_router
from models import db, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


@app.get("/ping", tags=["test"])
async def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
