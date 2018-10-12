from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, Http404

from task_list.mixin import LoginRequiredMixin
from task_list.models import Task, User


class TaskCrud(LoginRequiredMixin, TemplateView):
    valid_methods = ['create', 'edit', 'delete', 'done', 'undone']

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, *args, **kwargs):
        user = self._get_user(request)
        method = self._get_request_method(kwargs)

        if method == 'create':
            task_name = self._get_task_name(request)
            self._create_task(user, task_name)
        else:
            task = self._get_edited_task(request)
            if method == 'edit':
                task_name = self._get_task_name(request)
                self._edit_task(task.id, task_name, user)
            elif method == 'delete':
                self._delete_task(task, user)
            elif method == 'done':
                self._mark_as_done(task, user)
            elif method == 'undone':
                self._mark_as_undone(task)
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')

        return render(request, 'index.html', {})

    def _get_user(self, request):
        return request.user

    def _get_request_method(self, kwargs):
        method = kwargs.get('method', '')
        if method not in self.valid_methods:
            raise Http404
        return method

    def _get_edited_task(self, request) -> Task:
        task_id = self._get_task_id(request)
        try:
            return Task.objects.get(id=task_id)
        except ObjectDoesNotExist:
            raise Http404

    def _get_task_id(self, request) -> int:
        if 'task_id' in request.POST:
            return request.POST['task_id']
        raise HttpResponseBadRequest

    def _get_task_name(self, request) -> str:
        if 'task_name' in request.POST:
            return request.POST['task_name']
        else:
            raise HttpResponseBadRequest

    def _create_task(self, user: User, name: str):
        Task(name=name, owner=user, is_done=False).save()

    def _edit_task(self, task_id: int, task_name: str, user: User):
        task = Task.objects.get(id=task_id)
        if task.can_modify(user):
            task.name = task_name
            task.save()

    def _delete_task(self, task: Task, user: User):
        if task.can_modify(user):
            task.delete()
        else:
            raise HttpResponseForbidden

    def _mark_as_done(self, task: Task, user: User):
        task.is_done = True
        task.marked_done_by = user
        task.save()

    def _mark_as_undone(self, task: Task):
        task.is_done = False
        task.marked_done_by = None
        task.save()
