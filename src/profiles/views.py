from django.shortcuts import render, get_object_or_404, redirect
from profiles.models import Profiles
from .forms import RegisterForm

def index(request):
    context = {'profiles': Profiles.objects.all().order_by('name')}
    return render(request, 'profiles/profiles.html', context)


def login(request):
    return render(request, 'profiles/sign_in.html')


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
            return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "profiles/register.html", {"form":form})