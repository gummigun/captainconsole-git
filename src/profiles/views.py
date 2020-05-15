from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout

from profiles.models import Profiles
from .forms import RegisterForm

def index(request):
    context = {'profiles': Profiles.objects.all().order_by('name')}
    return render(request, 'profiles/profiles.html', context)


def take_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, '')
    else:
        get_object_or_404(Profiles, pk=id)


def my_account(request):
    if request.user.is_authenticated:
        return render(request, 'profiles/my_account.html')
    else:
        return redirect("/profiles/login")


def take_logout(request):
    logout(request)
    return render(request, '')


# /profile/1
def get_profile_by_id(request, id):
    return render(request, 'profiles/profiles_details.html', {
        'profiles': get_object_or_404(Profiles, pk=id)
    })

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/profiles/login")
    else:
        form = RegisterForm()

    return render(response, "profiles/register.html", {"form":form})