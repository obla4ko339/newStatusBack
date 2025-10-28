from httpx import AsyncClient
from src.models.customers import Customer
from src.models.serure_objects import SecurityObject
from src.models.list_objects import ListObjects
from src.models.list_customers import ListCustomers
from src.models.list_events import ListEvents
from src.core.settings import settings
from datetime import datetime, timezone
from src.services.cnord import CnordClient
from fastapi import APIRouter, HTTPException

class SiteEvents(CnordClient):
    def __init__(self):
        super().__init__()
    
    # Получить список событий объекта (GET /api/SiteEvents) по ID объекта id
    async def getSiteEventsId(self, id:str):
        try:
            response = await self.client.get(f"/api/SiteEvents?id={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            # print(data)
            return data
        except Exception as error:
            print(f"getParts {error}")
            
    # получить события исходя из полученных параметров, фильтры
    async def getSiteEventsParams(self, filter:object, id:str):
        # print(filter)
        try:
            import json
            response = await self.client.request(
                                            method="GET",
                                            url = f"/api/SiteEvents?id={id}",
                                            headers={
                                                 "apiKey": settings.cnord.CNORD_API_KEY,
                                                 "Content-Type": "application/json"
                                                 },
                                            # content=b'{"ectWarning": "true","ectBypass": "false","ectDisarm": "false","ectArm": "false","ectRestore": "false","ectFault": "false","ectReset": "false","ectAlarm": "false","ectOther": "false"}'
                                            content=json.dumps(filter).encode('utf-8')
                                            )
            data = response.json()
            return data
        except Exception as error:
            raise HTTPException(
                status_code=404, 
                detail=f"Item not found {error}"
            ) 
        