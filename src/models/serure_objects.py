from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class SecurityObject(models.Model):
    Id = fields.UUIDField(pk=True)
    AccountNumber = fields.IntField()
    CloudObjectID = fields.IntField()
    Name = fields.CharField(max_length=255)
    ObjectPassword = fields.CharField(max_length=255)
    Address = fields.TextField()
    Phone1 = fields.CharField(max_length=50)
    Phone2 = fields.CharField(max_length=50, null=True)
    TypeName = fields.CharField(max_length=100)
    IsFire = fields.BooleanField()
    IsArm = fields.BooleanField()
    IsPanic = fields.BooleanField()
    DeviceTypeName = fields.CharField(max_length=100)
    EventTemplateName = fields.CharField(max_length=100)
    ContractNumber = fields.CharField(max_length=100)
    ContractPrice = fields.DecimalField(max_digits=10, decimal_places=2)
    MoneyBalance = fields.DecimalField(max_digits=10, decimal_places=2)
    PaymentDate = fields.DatetimeField()
    DebtInformLevel = fields.IntField()
    Disabled = fields.BooleanField()
    DisableReason = fields.IntField()
    DisableDate = fields.DatetimeField()
    AutoEnable = fields.BooleanField()
    AutoEnableDate = fields.DatetimeField()
    CustomersComment = fields.TextField()
    CommentForOperator = fields.TextField()
    CommentForGuard = fields.TextField()
    MapFileName = fields.CharField(max_length=255)
    WebLink = fields.CharField(max_length=255)
    ControlTime = fields.IntField()
    CTIgnoreSystemEvent = fields.BooleanField()
    IsStateArm = fields.BooleanField()
    IsStateAlarm = fields.BooleanField()
    IsStatePartArm = fields.BooleanField()
    StateArmDisArmDateTime = fields.DatetimeField()
    LastSync = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "security_objects"

    def __str__(self):
        return f"{self.Name} ({self.AccountNumber})"


# Pydantic models
SecurityObject_Pydantic = pydantic_model_creator(SecurityObject, name="SecurityObject")
SecurityObjectIn_Pydantic = pydantic_model_creator(
    SecurityObject, name="SecurityObjectIn", exclude_readonly=True
)