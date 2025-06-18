from httpx import AsyncClient
from src.models.customers import Customer
from src.models.serure_objects import SecurityObject
class CnordClient:
    def __init__(self):
        self.client = AsyncClient(base_url="http://localhost:9002")

    async def write_security_objects(self):
        """
        Запись или обновление объектов охраны в БД с охранного сервера
        """
        response = await self.client.get("/api/Objects")
        data = response.json()

        ids = [item["Id"] for item in data]
        objects = [SecurityObject(**item) for item in data]

        await SecurityObject.bulk_create(
            objects,
            on_conflict=["Id"],  
            update_fields=[ 
                "AccountNumber", "CloudObjectID", "Name", "ObjectPassword", "Address",
                "Phone1", "Phone2", "TypeName", "IsFire", "IsArm", "IsPanic",
                "DeviceTypeName", "EventTemplateName", "ContractNumber", "ContractPrice",
                "MoneyBalance", "PaymentDate", "DebtInformLevel", "Disabled", "DisableReason",
                "DisableDate", "AutoEnable", "AutoEnableDate", "CustomersComment",
                "CommentForOperator", "CommentForGuard", "MapFileName", "WebLink",
                "ControlTime", "CTIgnoreSystemEvent", "IsStateArm", "IsStateAlarm",
                "IsStatePartArm", "StateArmDisArmDateTime"
            ]
        )

        return {"inserted_or_updated": len(objects), "ids": ids}


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