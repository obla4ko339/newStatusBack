from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ListCustomers(models.Model):

    Id = fields.UUIDField(pk=True)
    OrderNumber = fields.IntField(null=True)
    UserNumber = fields.IntField(null=True)
    ObjCustName = fields.CharField(max_length=255, null=True)
    ObjCustTitle = fields.CharField(max_length=255, null=True)
    ObjCustPhone1 = fields.TextField(max_length=50, null=True)
    ObjCustPhone2 = fields.CharField(max_length=50, null=True)
    ObjCustPhone3 = fields.CharField(max_length=50, null=True)
    ObjCustPhone4 = fields.CharField(max_length=50, null=True)
    ObjCustPhone5 = fields.CharField(max_length=50, null=True)
    ObjCustAddress = fields.CharField(max_length=100, null=True)
    IsVisibleInCabinet = fields.BooleanField(null=True)
    ReclosingRequest = fields.CharField(max_length=100, null=True)
    ReclosingFailure = fields.CharField(max_length=100, null=True)
    PINCode = fields.CharField(max_length=100, null=True)





    class Meta:
        table = "list_customers"
        database = "default"

    def __str__(self):
        return f"{self.Name} ({self.AccountNumber})"


# Pydantic models
ListCustomers_Pydantic = pydantic_model_creator(ListCustomers, name="ListCustomers")
ListCustomersIn_Pydantic = pydantic_model_creator(
    ListCustomers, name="ListCustomersIn", exclude_readonly=True
)