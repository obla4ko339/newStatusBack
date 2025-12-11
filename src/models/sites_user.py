from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib



class SitesUser(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    # object_id = fields.IntField()
    # create = fields.DatetimeField(auto_now_add=True)
    active = fields.BooleanField(default=True)

    # Добавляем связь с Sites
    site = fields.ForeignKeyField(
        'models.Sites', 
        related_name='site_users',
        on_delete=fields.CASCADE,
        source_field='object_id',
        to_field='AccountNumber'
    )
    
  
    class Meta:
        table = "user_object"





# SitesUser_Pydantic = pydantic_model_creator(SitesUser, name="SitesUser")
# SitesUserIn_Pydantic = pydantic_model_creator(SitesUser, name="SitesUserIn", exclude_readonly=True)
