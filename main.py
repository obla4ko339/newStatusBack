
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.services.tasks import start,stop, weekly_data_sync
from tortoise.contrib.fastapi import register_tortoise
from src.core.db import TORTOISE_ORM
from src.api.v1.router import router
from src.services.cnord import CnordClient
from src.services.sites import Sites
from src.services.parts import Parts
from src.services.zones import Zones
from src.services.siteEvents import SiteEvents
from src.services.events import Events
from src.services.siteSchedule import SiteSchedule
from src.services.customers import Customers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from fastapi.middleware.cors import CORSMiddleware


 
# @asynccontextmanager
# async def lifespan(app: FastAPI): 
#     start()
#     yield
#     stop() 
 
 
 
    
   
# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или "*" для всех
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


# Выполнение по интервалу START
app.include_router(router)
scheduler = AsyncIOScheduler()
async def my_task():
    getData = CnordClient()

    # await getData.getSiteEvents()
@app.on_event("startup")
async def startup_event():
    scheduler.add_job(my_task, 'interval', seconds=10)
    scheduler.start()

# Выполнение по интервалу START


@app.get("/")
async def getEventsSites():
    print("DATA!!!")

# @app.post("/")
# async def getEventsSites():
#     print("DATA")

@app.post("/")
async def post_events_sites(request: Request):
    try:
        # Получаем данные из тела запроса
        data = await request.json()
        print("POST Data received:", data)
        
        # Возвращаем KISS-OFF подтверждение
        return {
            "status": "success", 
            "message": "Data received",
            "kissOff": True,
            "receivedData": data
        }
        
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}


@app.get("/update")
async def update_obj():
    getData = CnordClient()
    
    # Объекты
    # sites  = Sites()
    # await sites.getSites()  
    # await sites.getSitesID("3954d447-0ddf-4587-800a-8d8db681f7f2") 
    # await sites.setSites("Тестовый обект 777") 
    
    # await getData.getSiteEvents()
    # await getData.write_security_objects() 
    
    # Разделы
    # part = Parts()
    # await part.getParts("3954d447-0ddf-4587-800a-8d8db681f7f2")
    
    
    # Шлейфы
    # zone = Zones()
    # await zone.getZonesSiteId("855b7fef-6d19-4e2a-9865-4304b5298182")
    
    # Ответстыенные
    # customer = Customers()
    # await customer.getCustomersSiteId("855b7fef-6d19-4e2a-9865-4304b5298182")
    
    # Список событий объекта
    # siteEvent = SiteEvents()
    # await siteEvent.getSiteEventsId("367568c8-60d1-48e5-970b-ea5aa548efc2")
    
    # Получить события
    # event = Events()
    # await event.getEvents()
    # await event.getEventsId("367568c8-60d1-48e5-970b-ea5aa548efc2")
    
    
    # Получить события
    # siteSchedule = SiteSchedule()
    # await siteSchedule.getSiteScheduleSiteId("367568c8-60d1-48e5-970b-ea5aa548efc2")
    
    
  

# @app.get("/force-load")
# async def force_load():
#     await weekly_data_sync()
#     return {"message": "Data synced"}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # отключаем автогенерацию схем — используем миграции
    add_exception_handlers=True,
)
