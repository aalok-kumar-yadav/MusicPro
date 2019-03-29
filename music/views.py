"""
    Music view is routing and rendering url based pages
    with user & music context data, this section have both Generic &
    Function based views.
"""

from django.shortcuts import render
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views import View
from . import api_context_helper, auth_helper
from .models import LastPlayedAudio
from django.core.cache import cache
import time

# Home generic view for home page http request
class Index(View):

    def get(self, request):
        st = time.time()
        context_data = api_context_helper.get_recommended_song()
        print(time.time()-st)
        stt = time.time()
        last_played_count = LastPlayedAudio.objects.all().count()
        if last_played_count == 0:
            audio_instance = api_context_helper.get_audio_stream_info(context_data[0]['audio_id'])
            model_instance = LastPlayedAudio(title=audio_instance['title'], audio_id=audio_instance['audio_id'], description=audio_instance['description'], stream_url=audio_instance['stream_url'], thumbnail=audio_instance['thumbnail'])
            model_instance.save()
        print("second")

        print(time.time()-stt)
        context_data[0]['stream_url'] = LastPlayedAudio.objects.all()[0].stream_url
        print(context_data[0]['stream_url'])
        return render(request, 'index.html', {'data': context_data})

    def post(self, request):
        return render(request, 'index.html')


# Login Generic View for user login
class Login(View):

    def get(self, request):
        return render(request, 'login.html', {'form': "form", 'message': "Valid"})

    def post(self, request):

        if auth_helper.get_session_user(request) is None:
            return render(request, 'login.html', {'form': "form", 'message': "Invalid"})
        else:
            return redirect('home_view')


# Logout View For Ending Session Of Current User
def log_out(request):

    request.session.flush()
    return redirect('home_view')


# RegisterUser Generic View For Get And Post Method
class RegisterUser(View):

    def get(self, request):
        return render(request, 'register.html', {'signup_form': "form", 'message': 'Valid'})

    def post(self, request):

        try:
            user_instance = User.objects.create_user(request.POST.get('Username'), request.POST.get('Email'),
                                                     request.POST.get('Password'))
            user_instance.first_name = request.POST.get('Name')
            user_instance.save()

            return redirect('home_view')

        except IntegrityError:
            return render(request, 'register.html',
                          {'signup_form': "form", 'message': 'Invalid'})
