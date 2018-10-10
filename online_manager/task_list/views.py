from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models.query import QuerySet

from task_list.mixin import LoginRequiredMixin
from task_list.models import Task, User


class FilteredTasks:
    pending_by_user: QuerySet
    pending_by_others: QuerySet
    done_by_user: QuerySet
    done_by_others: QuerySet

    user: User

    def __init__(self, user: User):
        self.user = user
        self._get_all_tasks()

    def _get_all_tasks(self):
        self._get_pending_tasks_by_user()
        self._get_pending_tasks_by_others()
        self._get_done_tasks_by_user()
        self._get_done_tasks_by_others()

    def _get_pending_tasks_by_user(self):
        self.pending_by_user = Task.objects.filter(owner=self.user, is_done=False)

    def _get_pending_tasks_by_others(self):
        self.pending_by_others = Task.objects.filter(is_done=False).exclude(owner=self.user)

    def _get_done_tasks_by_user(self):
        self.done_by_user = Task.objects.filter(owner=self.user, is_done=True)

    def _get_done_tasks_by_others(self):
        self.done_by_others = Task.objects.filter(is_done=True).exclude(owner=self.user)

    def to_dict(self):
        return {'mine_pending': self._query_to_dict(self.pending_by_user),
                'others_pending': self._query_to_dict(self.pending_by_others),
                'mine_done': self._query_to_dict(self.done_by_user),
                'others_done': self._query_to_dict(self.done_by_others),
                }

    def _query_to_dict(self, tasks: QuerySet):
        return [task.to_dict() for task in tasks]


class Index(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        tasks = FilteredTasks(request.user)
        return render(request, 'index.html', {'filtered_tasks': tasks.to_dict()})

    def post(self, request, *args, **kwargs):
        pass
