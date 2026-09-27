from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class UserGroupRight(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    section = fields.CharField(max_length=255)
    key = fields.CharField(max_length=255)
    description = fields.TextField(max_length=255)

    
    class Meta:
        table = "user_group_right"


