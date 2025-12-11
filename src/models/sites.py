from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class Sites(models.Model):
    id = fields.IntField(pk=True)
    Id = fields.CharField(max_length=255,unique=True)
    AccountNumber = fields.IntField(unique=True)
    CloudObjectID = fields.IntField()
    Name = fields.CharField(max_length=255)
    Address = fields.CharField(max_length=255)
    Phone1 = fields.CharField(max_length=255)
    Phone2 = fields.CharField(max_length=255)
    TypeName = fields.CharField(max_length=255)
    EventTemplateName = fields.CharField(max_length=255)
    
    

    class Meta:
        table = "sites"
        unique_together = (("Id","AccountNumber"),)


# SitesUser_Pydantic = pydantic_model_creator(SitesUser, name="SitesUser")
# SitesUserIn_Pydantic = pydantic_model_creator(SitesUser, name="SitesUserIn", exclude_readonly=True)
