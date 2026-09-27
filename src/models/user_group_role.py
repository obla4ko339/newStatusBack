from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class UserGroupRole(models.Model):
    id = fields.IntField(pk=True)
    user_group_id = fields.IntField()
    user_group_right_id = fields.IntField()
    
    class Meta:
        table = "user_group_role"


