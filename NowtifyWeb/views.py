from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User


# Create your views here.
def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, "web/login.html", {})


def logout(request):
    auth_logout(request)
    c = {}
    c.update(csrf(request))
    return render(request, "web/login.html", {})


def authentication(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:

        if user.is_active:
            auth_login(request, user)
            return redirect('overview')
        else:
            c = {}
            c.update(csrf(request))
            return render(request, "web/login.html", {})
    elif user is None:
        c = {}
        c.update(csrf(request))
        return render(request, "web/login.html", {})


@login_required(login_url='')
def change_password(request):

    c = {}
    c.update(csrf(request))

    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    current_user = request.user
    current_user_id = current_user.get_username()
    #current_user.get_username()

    if confirm_password == new_password:

        u = User.objects.get(username=current_user_id)
        u.set_password(new_password)
        u.save()

        return render(request, 'web/overview.html', {})

    else:
        #need Josie and Shawn to add error message instead of redirecting to overview page
        return render(request, 'web/overview.html', {})


@login_required(login_url='')
def index(request):
    return render(request, "web/index.html")


@login_required(login_url='')
def overview(request):
    return render(request, "web/overview.html")


@login_required(login_url='')
def sensor(request):
    return render(request, "web/sensor.html")


@login_required(login_url='')
def wearable(request):
    return render(request, "web/wearable.html")


@login_required(login_url='')
def dashboard(request):
    return render(request, "web/dashboard.html")


@login_required(login_url='')
def settings(request):
    return render(request, "web/settings.html")


@login_required(login_url='')
def alert(request):
    return render(request, "web/alert.html")


def handler404(request):
    response = render_to_response('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 404
    return response