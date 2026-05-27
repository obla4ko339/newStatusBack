from httpx import AsyncClient
from src.models.customers import Customer
from src.models.serure_objects import SecurityObject
from src.models.list_objects import ListObjects
from src.models.list_customers import ListCustomers
from src.models.list_events import ListEvents
from src.core.settings import settings
from datetime import datetime, timezone
from src.services.cnord import CnordClient

class SecurityObjectSection(CnordClient):
    def __init__(self):
        super().__init__()
        
        

    # /api/Sites/Arm
    async def isObjectSecurityArm(self, id:str):
        try:
            response = await self.client.post(f"/api/Sites/Arm?id={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            return response
        except Exception as error:   
            print(f"Exception: {error}")
            return error

    # /api/Sites/Disarm
    async def isObjectSecurityDisarm(self, id:str):
        try:
            response = await self.client.post(f"/api/Sites/Disarm?id={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            # data = response.json()
            print(response)
        except Exception as error:
            return error