from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import hashlib

class VerificationCode(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255)
    code_hash = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    used = fields.BooleanField(default=False)
    ip_address = fields.CharField(max_length=60)

    class Meta:
        table = "verification_codes"
        # unique_together = (("phone", "dogovor"),)


    def verify_code(self, code:str)->bool:
        hash_code = hashlib.md5(code.encode()).hexdigest()
        return hash_code == self.code_hash

    @staticmethod
    def hash_code(code:str) ->str:
        return hashlib.md5(code.encode()).hexdigest()

