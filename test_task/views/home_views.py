from django.shortcuts import render
from django.views import View

from ..models import Collection, Link


class HomeView(View):
    def get(self, request):
        collections = Collection.objects.filter(user=request.user)
        links = Link.objects.filter(user=request.user)
        return render(request, 'home.html', {
            'collections': collections,
            'links': links
        })
