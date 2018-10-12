from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse

from task_list.mixin import LoginRequiredMixin
from task_list.models import Task, User


class CrudHandler:
    user: User
    method: str
    task_id: int
    task_name: str
    valid_methods = ['create', 'edit', 'delete', 'done', 'undone']

    def __init__(self, user: User, method: str):
        self.user = user
        self.method = method

    def set_data(self, task_id: int = None, task_name: str = None):
        self.task_id = task_id
        self.task_name = task_name

    def exec_method(self):
        if self.method not in self.valid_methods:
            return HttpResponseBadRequest()
        else:
            if self.method == 'create':
                return self._exec_method_create()

            if self.task_id is None:
                return HttpResponseBadRequest()
            try:
                task_to_modify = Task.objects.get(id=self.task_id)
            except ObjectDoesNotExist:
                return HttpResponseNotFound()

            if self.method == 'done':
                return self._mark_as_done(task_to_modify)
            if self.method == 'undone':
                return self._mark_as_undone(task_to_modify)
            if self.method == 'delete':
                return self._delete_task(task_to_modify)

            if self.task_name is None:
                return HttpResponseBadRequest()
            if self.method == 'edit':
                return self._edit_task(task_to_modify)

    def _exec_method_create(self):
        if self.task_name is None:
            return HttpResponseBadRequest()
        else:
            self._create_task()
            return HttpResponse()

    def _create_task(self):
        Task(name=self.task_name, owner=self.user, is_done=False).save()

    def _edit_task(self, task: Task):
        if task.can_modify(self.user):
            task.name = self.task_name
            task.save()
            return HttpResponse()
        else:
            return HttpResponseForbidden()

    def _delete_task(self, task: Task):
        if task.can_modify(self.user):
            task.delete()
            return HttpResponse()
        else:
            return HttpResponseForbidden()

    def _mark_as_done(self, task: Task):
        task.is_done = True
        task.marked_done_by = self.user
        task.save()
        return HttpResponse()

    def _mark_as_undone(self, task: Task):
        task.is_done = False
        task.marked_done_by = None
        task.save()
        return HttpResponse()


class TaskCrud(LoginRequiredMixin, TemplateView):
    valid_methods = ['create', 'edit', 'delete', 'done', 'undone']

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, *args, **kwargs):
        user = self._get_user(request)
        method = self._get_request_method(kwargs)
        task_id = self._get_task_id(request)
        task_name = self._get_task_name(request)

        crud_handler = CrudHandler(user, method)
        crud_handler.set_data(task_id, task_name)

        return crud_handler.exec_method()

    def _get_user(self, request):
        return request.user

    def _get_request_method(self, kwargs):
        method = kwargs.get('method', '')
        return method

    def _get_task_id(self, request) -> int:
        return request.POST.get('task_id', None)

    def _get_task_name(self, request) -> str:
        return request.POST.get('task_name', None)
