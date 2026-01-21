from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class GroupUser(models.Model):
    id = fields.IntField(pk=True)
    name_group = fields.CharField(max_length=255)

    
    class Meta:
        table = "group_user"


