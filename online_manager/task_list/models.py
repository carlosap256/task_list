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
    marked_done_by = models.ForeignKey(User, related_name='done_by', null=True, on_delete=models.DO_NOTHING)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner.to_dict(),
            'is_done': self.is_done,
            'marked_done_by': self.marked_done_by.to_dict() if self.marked_done_by else ''
        }

    def can_modify(self, user:User):
        return self.owner.id == user.id
