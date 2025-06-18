from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.services.tasks import start,stop, weekly_data_sync
from tortoise.contrib.fastapi import register_tortoise
from src.core.db import TORTOISE_ORM
from src.api.v1.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    start()
    yield
    stop()

    
app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/force-load")
def force_load():
    weekly_data_sync()
    return {"message": "Data synced"}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # отключаем автогенерацию схем — используем миграции
    add_exception_handlers=True,
)
