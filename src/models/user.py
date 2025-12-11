from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    group_user = fields.IntField(null=False)
    email = fields.CharField(max_length=100)
    tel = fields.CharField(max_length=50)
    parent = fields.IntField(null=True)

    class Meta:
        table = "users"

    def verify_password(self, password: str) -> bool:
        # Используем простой MD5 хеш для демонстрации
        password_hash = hashlib.md5(password.encode()).hexdigest()
        return password_hash == self.password_hash

    @staticmethod
    def hash_password(password: str) -> str:
        # Используем простой MD5 хеш для демонстрации
        return hashlib.md5(password.encode()).hexdigest()

    def __str__(self):
        return f"User {self.username}"

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
