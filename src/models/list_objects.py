from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ListObjects(models.Model):

    RowNumber = fields.IntField()
    Id = fields.UUIDField(pk=True)
    AccountNumber = fields.IntField(null=True)
    CloudObjectID = fields.IntField(null=True)
    Name = fields.CharField(max_length=255, null=True)
    ObjectPassword = fields.CharField(max_length=255, null=True)
    Address = fields.TextField(null=True)
    Phone1 = fields.CharField(max_length=50, null=True)
    Phone2 = fields.CharField(max_length=50, null=True)
    TypeName = fields.CharField(max_length=100, null=True)
    IsFire = fields.BooleanField(null=True)
    IsArm = fields.BooleanField(null=True)
    IsPanic = fields.BooleanField(null=True)
    DeviceTypeName = fields.CharField(max_length=100, null=True)
    EventTemplateName = fields.CharField(max_length=100, null=True)
    ContractNumber = fields.CharField(max_length=100, null=True)
    ContractPrice = fields.DecimalField(max_digits=10, decimal_places=2, default=None, null=True,blank=True)
    MoneyBalance = fields.DecimalField(max_digits=10, decimal_places=2, default=None, null=True,blank=True)
    PaymentDate = fields.DatetimeField(null=True)
    DebtInformLevel = fields.IntField(null=True)
    Disabled = fields.BooleanField(null=True)
    DisableReason = fields.IntField(null=True)
    DisableDate = fields.DatetimeField(null=True)
    AutoEnable = fields.BooleanField(null=True)
    AutoEnableDate = fields.DatetimeField(null=True)
    CustomersComment = fields.TextField(null=True)
    CommentForOperator = fields.TextField(null=True)
    CommentForGuard = fields.TextField(null=True)
    MapFileName = fields.CharField(max_length=255, null=True)
    WebLink = fields.CharField(max_length=255, null=True)
    ControlTime = fields.IntField(null=True)
    CTIgnoreSystemEvent = fields.BooleanField(null=True)
    IsStateArm = fields.BooleanField(null=True)
    IsStateAlarm = fields.BooleanField(null=True)
    IsStatePartArm = fields.BooleanField(null=True)
    StateArmDisArmDateTime = fields.DatetimeField(null=True)



    class Meta:
        table = "list_objects"
        database = "default"

    def __str__(self):
        return f"{self.Name} ({self.AccountNumber})"


# Pydantic models
ListObjects_Pydantic = pydantic_model_creator(ListObjects, name="ListObjects")
ListObjectsIn_Pydantic = pydantic_model_creator(
    ListObjects, name="ListObjectsIn", exclude_readonly=True
)