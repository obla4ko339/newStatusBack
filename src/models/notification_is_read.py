from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib
from src.models.notification import Notification

class NotificationIsRead(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(null=True)
    # message_id = fields.IntField(null=True)
    message_id = fields.ForeignKeyField( 
        model_name="models.Notification",
        related_name="message_item",
        on_delete = fields.RESTRICT,
        source_field="message_id" 
        )
    is_read = fields.BooleanField(default=False, null=True)
    
    class Meta:
        table = "notification_is_read"



