from django.views.generic import TemplateView
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import timezone

from task_list.models import Task, User


class TaskCrud(TemplateView):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, *args, **kwargs):
        post_items = dict(request.POST)
        if 'id' in post_items:
            task_id = post_items['id']
            task = Task.objects.get(id=task_id)

        method = kwargs.get('method', '')
        if method == 'create':
            pass
        elif method == 'delete':
            pass
        elif method == 'done':
            pass
        elif method == 'undone':
            pass
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return render(request, 'index.html', {})
