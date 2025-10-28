from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Customer(models.Model):
    Id = fields.UUIDField(pk=True)
    OrderNumber = fields.IntField()
    UserNumber = fields.IntField()
    ObjCustName = fields.CharField(max_length=255)
    ObjCustTitle = fields.CharField(max_length=255)
    ObjCustPhone1 = fields.CharField(max_length=50)
    ObjCustPhone2 = fields.CharField(max_length=50, null=True)
    ObjCustPhone3 = fields.CharField(max_length=50, null=True)
    ObjCustPhone4 = fields.CharField(max_length=50, null=True)
    ObjCustPhone5 = fields.CharField(max_length=50, null=True)
    ObjCustAddress = fields.TextField()
    IsVisibleInCabinet = fields.BooleanField(default=True)
    ReclosingRequest = fields.BooleanField(default=False)
    ReclosingFailure = fields.BooleanField(default=False)
    PINCode = fields.CharField(max_length=50)
    LastSync = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "customers"

    def __str__(self):
        return f"{self.ObjCustName} ({self.OrderNumber})"


# Pydantic models
Customer_Pydantic = pydantic_model_creator(Customer, name="Customer")
CustomerIn_Pydantic = pydantic_model_creator(
    Customer, name="CustomerIn", exclude_readonly=True
)