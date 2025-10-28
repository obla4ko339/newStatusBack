from httpx import AsyncClient
from src.models.customers import Customer
from src.models.serure_objects import SecurityObject
from src.models.list_objects import ListObjects
from src.models.list_customers import ListCustomers
from src.models.list_events import ListEvents
from src.core.settings import settings
from datetime import datetime, timezone

class CnordClient:
    def __init__(self):
        self.client = AsyncClient(base_url=f"http://{settings.cnord.CNORD_URL}:{settings.cnord.CNORD_PORT}")


    

    async def getSites(self):
        
        """
        Запись или обновление объектов охраны в БД с охранного сервера
        """
        response = await self.client.get("/api/Sites",headers={"apiKey": settings.cnord.CNORD_API_KEY},)
        data = response.json()
        
        ids = [item["Id"] for item in data]
        
        # objects = [SecurityObject(**item) for item in data]
        objects = []
        for item in data:
            try:
                date_fields = ['PaymentDate', 'DisableDate', 'AutoEnableDate', 'StateArmDisArmDateTime']
                for field in date_fields:
                    if item[field] == '1899-12-30T00:00:00':
                        item[field] = None
                    else:
                        dt_str = item[field].replace('Z', '+00:00')
                        item[field] = datetime.fromisoformat(dt_str).astimezone(timezone.utc)
                objects.append(ListObjects(**item))
            except Exception as err:
                print(f"ошибка в элементе {item}", err)
        # return False

        await ListObjects.bulk_create(
            objects
        )


    

    async def getSiteEvents(self, id:str):
        # Получить список ответственных лиц объекта тут будет подставлять ID
        response = await self.client.get("/api/SiteEvents?id="+id, headers={"apiKey": settings.cnord.CNORD_API_KEY})
        
        data = response.json() 
        # print(data)
        
        # return False
        objects = []
        for item in data:
            try:
                objects.append(ListEvents(**item))
            except Exception as err:
                print(f"Ошибка в строк {item}", err)

        await ListEvents.bulk_create(
            objects
        )
            



    async def write_customers(self, site_id: str):
        """
        Запись или обновление ответственных лиц в БД с охранного сервера
        """
        response = await self.client.get("/api/Customers", params={"siteID": site_id})
        data = response.json()

        customers = [Customer(**item) for item in data]

        await Customer.bulk_create(
            customers,
            on_conflict=["Id"],  
            update_fields=[
                "OrderNumber", "UserNumber", "ObjCustName", "ObjCustTitle",
                "ObjCustPhone1", "ObjCustPhone2", "ObjCustPhone3", "ObjCustPhone4", "ObjCustPhone5",
                "ObjCustAddress", "IsVisibleInCabinet", "ReclosingRequest",
                "ReclosingFailure", "PINCode"
            ]
        )

        return {"inserted_or_updated": len(customers)}