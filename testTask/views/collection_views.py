from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..forms import CollectionForm
from ..models import Collection


class CollectionListView(View):
    @swagger_auto_schema(
        operation_description="Get the list of collections for the authenticated user.",
        responses={
            200: openapi.Response(description="A list of collections")
        }
    )
    def get(self, request):
        collections = Collection.objects.filter(user=request.user)
        return render(request, 'collection_list.html', {'collections': collections})


class CollectionCreateView(View):
    @swagger_auto_schema(
        operation_description="Create a new collection for the authenticated user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Collection name'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Collection description'),
            }
        ),
        responses={
            200: openapi.Response(description="Redirect to home page"),
            400: openapi.Response(description="Invalid collection data")
        }
    )
    def get(self, request):
        form = CollectionForm()
        return render(request, 'collection_form.html', {'form': form})

    def post(self, request):
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            return redirect('home')
        return render(request, 'collection_form.html', {'form': form})


class CollectionUpdateView(View):
    @swagger_auto_schema(
        operation_description="Update an existing collection for the authenticated user.",
        request_body=CollectionForm,
        responses={
            200: openapi.Response(description="Collection successfully updated and redirected to home page"),
            400: openapi.Response(description="Invalid collection data"),
            404: openapi.Response(description="Collection not found")
        }
    )
    def get(self, request, pk):
        collection = Collection.objects.get(pk=pk, user=request.user)
        form = CollectionForm(instance=collection)
        return render(request, 'collection_form.html', {'form': form})

    def post(self, request, pk):
        collection = Collection.objects.get(pk=pk, user=request.user)
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'collection_form.html', {'form': form})


class CollectionDeleteView(View):
    @swagger_auto_schema(
        operation_description="Delete an existing collection for the authenticated user.",
        responses={
            200: openapi.Response(description="Collection successfully deleted and redirected to home page"),
            404: openapi.Response(description="Collection not found")
        }
    )
    def get(self, request, pk):
        collection = Collection.objects.get(pk=pk, user=request.user)
        collection.delete()
        return redirect('home')


class CollectionRemoveLinkView(View):
    @swagger_auto_schema(
        operation_description="Remove a link from a collection.",
        responses={
            200: openapi.Response(description="Link successfully removed from collection"),
            404: openapi.Response(description="Collection or Link not found")
        }
    )
    def post(self, request, collection_id, link_id):
        collection = get_object_or_404(Collection, id=collection_id, user=request.user)
        collection.links.remove(link_id)
        return redirect('collection_detail', pk=collection_id)
