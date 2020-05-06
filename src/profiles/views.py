from django.shortcuts import render, get_object_or_404
from products.models import Products


def index(request):
    context = {'profiles': Profiles.objects.all().order_by('name')}
    return render(request, 'profiles/profiles.html', context)

# /profile/1
def get_profile_by_id(request, id):
    return render(request, 'profiles/profiles_details.html', {
        'profiles': get_object_or_404(Profiles, pk=id)
    })
