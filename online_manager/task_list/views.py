from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


class Index(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})

    def post(self, request, *args, **kwargs):
        pass
