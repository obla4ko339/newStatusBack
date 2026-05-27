from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class NotificationType(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    color = fields.CharField(max_length=255, null=True)
    
    class Meta:
        table = "notification_type"



