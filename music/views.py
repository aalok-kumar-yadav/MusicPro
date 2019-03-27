"""
    Music view is routing and rendering url based pages
    with user & music context data, this section have both Generic &
    Function based views.
"""

from django.shortcuts import render
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.db import IntegrityError
from django.views import View


# Home generic view for home page http request
class Index(View):

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        return render(request, 'index.html')


