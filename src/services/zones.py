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
        