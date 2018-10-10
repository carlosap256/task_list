from typing import List, Dict

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from task_list.models import Task, User


class TaskList:
    pending_by_user: List[Dict[str, object]]
    pending_by_others: List[Dict[str, object]]
    done_by_user: List[Dict[str, object]]
    done_by_other: List[Dict[str, object]]


class Index(TemplateView):
    task_list: TaskList

    def get(self, request, *args, **kwargs):
        tasks = self._get_tasks()
        return render(request, 'index.html', {'tasks': tasks})

    def _get_tasks(self):
        tasks = Task.objects.all()
        return [task.to_dict() for task in tasks]

    def post(self, request, *args, **kwargs):
        pass
