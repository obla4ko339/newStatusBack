from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib
from src.models.notification_type import NotificationType

class Notification(models.Model):
    id = fields.IntField(pk=True)
    create_at = fields.DatetimeField(max_length=255, null=True)
    message = fields.TextField(max_length=255)
    user_id_from = fields.IntField(null=True)
    user_id_to = fields.JSONField(max_length=255, null=True)
    type = fields.IntField(null=True)
    # type = fields.ForeignKeyField( 
    #     model_name="NotificationType",
    #     related_name="notifications",
    #     on_delete = fields.RESTRICT
    # )
    status = fields.BooleanField(default=False, null=True)

    
    class Meta:
        table = "notification"



