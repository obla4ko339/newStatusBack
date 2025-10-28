from httpx import AsyncClient
from src.models.customers import Customer
from src.models.serure_objects import SecurityObject
from src.models.list_objects import ListObjects
from src.models.list_customers import ListCustomers
from src.models.list_events import ListEvents
from src.core.settings import settings
from datetime import datetime, timezone
from src.services.cnord import CnordClient

class Sites(CnordClient):
    def __init__(self):
        # self.client = AsyncClient(base_url=f"http://{settings.cnord.CNORD_URL}:{settings.cnord.CNORD_PORT}")
        super().__init__()
        
        

    async def getSite(self, data):
        if not data:
            return False
        try:
            response = await self.client.get("/api/Sites",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            return data
        except Exception as error:
            return error
    
    async def getSitesOUT(self, data):
        
        """
        Запись или обновление объектов охраны в БД с охранного сервера
        """
        try:
            response = await self.client.get("/api/Sites",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            
            ids = [item["Id"] for item in data]
            
            # objects = [SecurityObject(**item) for item in data]
            objects = []
            for item in data:
                try:
                    date_fields = ['PaymentDate', 'DisableDate', 'AutoEnableDate', 'StateArmDisArmDateTime']
                    for field in date_fields:
                        if item[field] is not None:
                            if item[field] == '1899-12-30T00:00:00':
                                item[field] = None
                            else:
                                dt_str = item[field].replace('Z', '+00:00')
                                item[field] = datetime.fromisoformat(dt_str).astimezone(timezone.utc)
                        else:
                            item[field] = None  # Явно сохраняем None
                    objects.append(ListObjects(**item))
                except Exception as err:
                    print(f"ошибка в элементе {item}", err)
            # return False

            await ListObjects.bulk_create(
                objects
            )
        except Exception as error:
            print(f" getSites {error}")
            return error

    async def getSites(self):
        
        """
        Запись или обновление объектов охраны в БД с охранного сервера
        """
        try:
            response = await self.client.get("/api/Sites",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            
            ids = [item["Id"] for item in data]
            
            # objects = [SecurityObject(**item) for item in data]
            objects = []
            for item in data:
                try:
                    date_fields = ['PaymentDate', 'DisableDate', 'AutoEnableDate', 'StateArmDisArmDateTime']
                    for field in date_fields:
                        if item[field] is not None:
                            if item[field] == '1899-12-30T00:00:00':
                                item[field] = None
                            else:
                                dt_str = item[field].replace('Z', '+00:00')
                                item[field] = datetime.fromisoformat(dt_str).astimezone(timezone.utc)
                        else:
                            item[field] = None  # Явно сохраняем None
                    objects.append(ListObjects(**item))
                except Exception as err:
                    print(f"ошибка в элементе {item}", err)
            # return False

            await ListObjects.bulk_create(
                objects
            )
        except Exception as error:
            print(f" getSites {error}")
            return error
    
    
    # Получить объект по номеру или идентификатору
    async def getSitesID(self, id:str):
        try:
            response = await self.client.get(f"/api/Sites?id={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
            data = response.json()
            return data
        except Exception as error:
            print(f"getSitesID {error}")
            
    
    # Получить объект по имени
    async def getSitesFilter(self, filter:object):
        print(filter)
        print({
                                                 "apiKey": settings.cnord.CNORD_API_KEY,
                                                 "Content-Type": "application/json"
                                                 })
        if bool(filter) == False:
            return False
        try:
            import json
            response = await self.client.request(
                                            method="GET",
                                            url = f"/api/Sites",
                                            headers={
                                                 "apiKey": settings.cnord.CNORD_API_KEY,
                                                 "Content-Type": "application/json"
                                                 },
                                            # content=b'{"ectWarning": "true","ectBypass": "false","ectDisarm": "false","ectArm": "false","ectRestore": "false","ectFault": "false","ectReset": "false","ectAlarm": "false","ectOther": "false"}'
                                            content=json.dumps(filter).encode('utf-8')
                                            )
            data = response.json()
            print(data)
            return data
        except Exception as error:
            print(f"getSitesFilter error: {error}")
            print(f"Error type: {type(error)}")
            print(f"getSitesFilter error: {error}")
            print(f"Trying to connect to: {settings.cnord.CNORD_URL}:{settings.cnord.CNORD_PORT}")
            if hasattr(error, 'response'):
                print(f"Response status: {error.response.status_code}")
                print(f"Response text: {error.response.text}")
            return None
    
    
    # Создать объект (POST /api/Sites)
    async def setSites(self, name:object):
        print(name)
        # return False
        try:
            response = await self.client.post(f"/api/Sites",headers={"apiKey": settings.cnord.CNORD_API_KEY}, data={"Name":name.get('nameSites')})
            data = response.json()
            return data
        except Exception as error:
            print(f"getSitesID {error}")
        
        
        
    # Удалить объект (DELETE /api/Sites)
    async def deleteSites(self, id:str):
        try:
            response = await self.client.delete(f"/api/Sites?id={id}",headers={"apiKey": settings.cnord.CNORD_API_KEY}, data={"Name":name})
            data = response.json()
            return data
        except Exception as error:
            print(f"getSitesID {error}")
            
