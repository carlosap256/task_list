from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from task_list.models import Task, User


class Index(TemplateView):

    def get(self, request, *args, **kwargs):
        tasks = self._get_tasks()
        return render(request, 'index.html', {'tasks': tasks})

    def _get_tasks(self):
        tasks = Task.objects.all()
        return [task.to_dict() for task in tasks]

    def post(self, request, *args, **kwargs):
        pass
