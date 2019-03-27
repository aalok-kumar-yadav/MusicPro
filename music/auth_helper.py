"""
    Authorization helper is for user authentication & user registration
    there are helper function for Authorizing user.
"""

from django.contrib.auth import authenticate


# get_session_user function for getting session user
def get_session_user(request):
    username = None

    if request.method == 'GET':

        if 'username' in request.session:
            username = request.session['username']

    elif request.method == 'POST':

        form_login = ""

        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            auth_var = authenticate(username=form_login.cleaned_data['username'],
                                    password=form_login.cleaned_data['password'])

            if auth_var is not None:
                request.session['username'] = username
            else:
                username = None

    return username  # Returning Username

