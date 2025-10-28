from httpx import AsyncClient
from src.models.customers import Customer
from src.models.serure_objects import SecurityObject
from src.models.list_objects import ListObjects
from src.models.list_customers import ListCustomers
from src.models.list_events import ListEvents
from src.core.settings import settings
from datetime import datetime, timezone
from src.services.cnord import CnordClient

class Events(CnordClient):
    def __init__(self):
        super().__init__()
    
    # Получить список событий (GET /api/Events) по ID объекта id
    # Метод, предназначенный для получения событий. Метод возвращает не только события переданные охранным
    # приборами, но и события сформированные программным обеспечением «Центр охраны».
    
    # Выведет все события
    async def getEvents(self):
        try:
            response = await self.client.get(f"/api/Events",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            print(data)
            return data
        except Exception as error:
            print(f"getParts {error}")
            
            
    
    # # Выведет все события по id объекта
    async def getEventsId(self, id:str):
        try:
            response = await self.client.get(f"/api/Events?id={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            print(data)
            return data
        except Exception as error:
            print(f"getParts {error}")
        