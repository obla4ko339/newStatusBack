from httpx import AsyncClient
from src.models.customers import Customer
from src.models.serure_objects import SecurityObject
from src.models.list_objects import ListObjects
from src.models.list_customers import ListCustomers
from src.models.list_events import ListEvents
from src.core.settings import settings
from datetime import datetime, timezone
from src.services.cnord import CnordClient

class Zones(CnordClient):
    def __init__(self):
        # self.client = AsyncClient(base_url=f"http://{settings.cnord.CNORD_URL}:{settings.cnord.CNORD_PORT}")
        super().__init__()
    
    # Получить список шлейфов объекта (GET /api/Zones) по ID объекта siteId
    async def getZonesSiteId(self, id:str):
        try:
            response = await self.client.get(f"/api/Parts?siteId={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            print(data)
            return data
        except Exception as error:
            print(f"getParts {error}")


    # Взять раздел под охрану (POST /api/Parts/Arm)
    async def isArmZoneApi(self, id:str):
        try:
            response = await self.client.post(f"/api/Parts/Arm?id={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            print(data)
            return data
        except Exception as error:
            print(f"getParts {error}")


    # Снять раздел с охраны (POST /api/Parts/Disarm)
    async def disArmZoneApi(self, id:str):
        try:
            response = await self.client.post(f"/api/Parts/Disarm?id={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            print(data)
            return data
        except Exception as error:
            print(f"getParts {error}")
        