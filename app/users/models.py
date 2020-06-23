from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    status = fields.IntField()
    username = fields.CharField(unique=True, max_length=100)
    password = fields.CharField(max_length=100)
    email = fields.CharField(unique=True, max_length=100)
    phone = fields.CharField(unique=True, max_length=10)

    class Meta:
        table = 'Users'

    def __str__(self):
        return self.username
