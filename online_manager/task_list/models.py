from django.db import models
from django.contrib.auth.models import User


User.add_to_class(
        'to_dict',
        lambda self: {
            "username": self.username,
        })


class Task(models.Model):
    name = models.CharField(default='', max_length=300, null=False)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_done = models.BooleanField(default=False)

    def to_dict(self):
        return {
            'name': self.name,
            'owner': self.owner.to_dict(),
            'is_done': self.is_done,
        }
