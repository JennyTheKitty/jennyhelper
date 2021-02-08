from tortoise.models import Model
from tortoise import fields


class RoleMessage(Model):
    id = fields.BigIntField(pk=True)
    data = fields.JSONField()

    def __str__(self):
        return 'RoleMessage[{}]'.format(self.id)
