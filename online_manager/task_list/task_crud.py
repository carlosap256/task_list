from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from django.utils import timezone

from task_list.models import Task, User


class TaskCrud(TemplateView):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, *args, **kwargs):
        user = self._get_user(request)
        method = self._get_request_method(kwargs)

        if method == 'create':
            self._create_task(user, 'Test task')
        else:
            task = self._get_edited_task(request)

            if method == 'delete':
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
        valid_methods = ['create', 'delete', 'done', 'undone']
        method = kwargs.get('method', '')
        if method not in valid_methods:
            raise HttpResponseBadRequest
        return method

    def _get_edited_task(self, request) -> Task:
        if 'task_id' in request.POST:
            task_id = request.POST['task_id']
            try:
                return Task.objects.get(id=task_id)
            except ObjectDoesNotExist:
                raise HttpResponseNotFound
        raise HttpResponseBadRequest

    def _create_task(self, user: User, name: str):
        pass

    def _delete_task(self, task: Task, user: User):
        if task.can_delete(user):
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
