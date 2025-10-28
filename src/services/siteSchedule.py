from httpx import AsyncClient
from src.models.customers import Customer
from src.models.serure_objects import SecurityObject
from src.models.list_objects import ListObjects
from src.models.list_customers import ListCustomers
from src.models.list_events import ListEvents
from src.core.settings import settings
from datetime import datetime, timezone
from src.services.cnord import CnordClient

class SiteSchedule(CnordClient):
    def __init__(self):
        super().__init__()
    
    # Получить расписание охраны объекта по ID объекта siteId
    async def getSiteScheduleSiteId(self, id:str):
        try:
            response = await self.client.get(f"/api/SiteSchedule?siteId={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            print(data)
            return data
        except Exception as error:
            print(f"getParts {error}")
            return error
        