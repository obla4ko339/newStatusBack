from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class SitesLocalInfo(models.Model):
    id = fields.IntField(pk=True)
    # sites_id = fields.IntField(unique=True)
    local_adress = fields.CharField(max_length=255)
    local_tel = fields.CharField(max_length=255)
    local_name = fields.CharField(max_length=255)
    create_at = fields.DatetimeField(auto_now_add=True)
    sites_id = fields.OneToOneField(
        model_name = "models.Sites", ##. модель с короой связываемся 
        to_field = "AccountNumber", ## с какого поля берем инфу для сравнения
        source_field="sites_id", ## чтобы не добавлялось _id
    )

    
    

    class Meta:
        table = "sites_local_info"
        # unique_together = (("Id","AccountNumber"),)


# SitesUser_Pydantic = pydantic_model_creator(SitesUser, name="SitesUser")
# SitesUserIn_Pydantic = pydantic_model_creator(SitesUser, name="SitesUserIn", exclude_readonly=True)
