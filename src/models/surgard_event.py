from tortoise import fields
from tortoise.models import Model


class EventCodes(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=10, unique=True)
    description_ru = fields.TextField()
    description_en = fields.TextField()
    group_category = fields.CharField(max_length=100)
    active = fields.BooleanField(default=True)
    
    class Meta:
        table = "event_codes"


class SurgardEvent(Model):
    id = fields.IntField(pk=True)
    account_number = fields.CharField(max_length=10, null=True)
    event_type = fields.CharField(max_length=10, null=True)
    event_code = fields.CharField(max_length=10, null=True)
    group_code = fields.CharField(max_length=10, null=True)
    zone_or_user = fields.CharField(max_length=10, null=True)
    datetime = fields.DatetimeField(null=True) 
    raw = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    

    class Meta:
        table = "surgard_events"