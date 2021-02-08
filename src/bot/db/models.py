from tortoise.models import Model
from tortoise import fields


class RoleMessage(Model):
    id = fields.BigIntField(pk=True)

    def __str__(self):
        return 'RoleMessage[{}]'.format(self.id)
