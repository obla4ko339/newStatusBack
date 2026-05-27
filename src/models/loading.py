from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class Loading1c(models.Model):
    id = fields.IntField(pk=True)
    phone = fields.CharField(max_length=255)
    dogovor = fields.CharField(max_length=255)
    dolg = fields.DecimalField(max_digits=20, decimal_places=2)
    pay = fields.DecimalField(max_digits=20, decimal_places=2,null=True)
    pre_pay = fields.IntField(null=True)
    bill_status = fields.BooleanField(null=True)
    # date = fields.CharField(max_length=255)
    date = fields.DatetimeField(max_length=255, null=True)
    user_loading = fields.IntField(null=True)
    


    
    class Meta:
        table = "loading_1c"
        unique_together = (("phone", "dogovor"),)


