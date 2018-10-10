from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def to_dict(self):
        return{
            "username": self.username,
        }


class Task(models.Model):
    name = models.CharField(default='', max_length=300, null=False)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    done = models.BooleanField(default=False)

    def to_dict(self):
        return {
            'name': self.name,
            'owner': self.owner.to_dict(),
            'done': self.done,
        }
