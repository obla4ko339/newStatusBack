from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class Logs(models.Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=255)
    desc = fields.TextField(max_length=255)
    ip = fields.CharField(max_length=255)
    section = fields.CharField(max_length=255)
    user = fields.IntField(null=True)
    date_create = fields.DatetimeField(max_length=255, null=True)

    
    class Meta:
        table = "logs"



