from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..forms import LinkForm
from ..models import Link
from ..utils import fetch_link_data


class LinkListView(View):
    @swagger_auto_schema(
        operation_description="Get a list of all links for the authenticated user.",
        responses={
            200: openapi.Response(description="List of links for the authenticated user"),
            404: openapi.Response(description="No links found for the user")
        }
    )
    def get(self, request):
        links = Link.objects.filter(user=request.user)
        return render(request, 'link_list.html', {'links': links})


class LinkCreateView(View):
    @swagger_auto_schema(
        operation_description="Create a new link for the authenticated user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(type=openapi.TYPE_STRING, description='URL of the link'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the link'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the link'),
            }
        ),
        responses={
            200: openapi.Response(description="Redirect to home page"),
            400: openapi.Response(description="Invalid URL or duplicate URL")
        }
    )
    def get(self, request):
        form = LinkForm()
        return render(request, 'link_form.html', {'form': form})

    def post(self, request):
        form = LinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            if Link.objects.filter(url=url, user=request.user).exists():
                form.add_error('url', 'This URL already exists in your collection.')
                return render(request, 'link_form.html', {'form': form})

            link_data = fetch_link_data(url)
            link = Link(
                url=url,
                title=link_data.get('title', ''),
                description=link_data.get('description', ''),
                user=request.user
            )
            link.save()
            return redirect('home')
        return render(request, 'link_form.html', {'form': form})


class LinkUpdateView(View):
    @swagger_auto_schema(
        operation_description="Update an existing link for the authenticated user.",
        request_body=LinkForm,
        responses={
            200: openapi.Response(description="Link successfully updated and redirected to home page"),
            400: openapi.Response(description="Invalid link data"),
            404: openapi.Response(description="Link not found")
        }
    )
    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        form = LinkForm(instance=link)
        return render(request, 'link_form.html', {'form': form})

    def post(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'link_form.html', {'form': form})


class LinkDeleteView(View):
    @swagger_auto_schema(
        operation_description="Delete an existing link for the authenticated user.",
        responses={
            200: openapi.Response(description="Link successfully deleted and redirected to home page"),
            404: openapi.Response(description="Link not found")
        }
    )
    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        link.delete()
        return redirect('home')
