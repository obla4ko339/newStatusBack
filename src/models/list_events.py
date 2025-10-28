from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ListEvents(models.Model):

    Id = fields.UUIDField(pk=True)
    RChannelName = fields.CharField(max_length=255, null=True)
    DateTime = fields.DatetimeField(null=True)
    AccountNumber = fields.IntField(null=True)
    EventCode = fields.CharField(max_length=255, null=True)
    EventClassName = fields.CharField(max_length=255, null=True)
    EventClassType = fields.CharField(max_length=255, null=True)
    EventDesc = fields.CharField(max_length=255, null=True)
    PartNumber = fields.IntField(null=True)
    ZoneUser = fields.IntField(null=True)
    AlarmIndex = fields.BigIntField(null=True)
    SaveDateTime = fields.DatetimeField(null=True)






    class Meta:
        table = "list_events"
        database = "default"

    def __str__(self):
        return f"{self.Name} ({self.AccountNumber})"


# Pydantic models
# ListEvents_Pydantic = pydantic_model_creator(ListEvents, name="ListEvents")
# ListEventsIn_Pydantic = pydantic_model_creator(
#     ListEvents, name="ListEventsIn", exclude_readonly=True
# )