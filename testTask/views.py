from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Link, Collection
from .forms import UserRegistrationForm, UserLoginForm, LinkForm, CollectionForm
from .utils import fetch_link_data
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserRegisterHTMLView(View):
    @swagger_auto_schema(
        operation_description="User registration endpoint.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            }
        ),
        responses={
            200: openapi.Response(description="Redirect to login page"),
            400: openapi.Response(description="Bad request (invalid form data)")
        }
    )
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class UserLoginHTMLView(View):
    @swagger_auto_schema(
        operation_description="User login endpoint.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            }
        ),
        responses={
            200: openapi.Response(description="Redirect to home page"),
            401: openapi.Response(description="Invalid username or password")
        }
    )
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        return render(request, 'login.html', {'form': form})

class UserLogoutView(View):
    @swagger_auto_schema(
        operation_description="User logout endpoint.",
        responses={
            200: openapi.Response(description="Redirect to login page")
        }
    )
    def post(self, request):
        logout(request)
        return redirect('login')

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
                title=link_data.get("title") or "No Title",
                description=link_data.get("description") or "No Description",
                image=link_data.get("image"),
                user=request.user
            )
            link.save()

            return redirect('home')
        return render(request, 'link_form.html', {'form': form})

class LinkUpdateView(View):
    @swagger_auto_schema(
        operation_description="Update an existing link for the authenticated user.",
        responses={
            200: openapi.Response(description="Redirect to home page"),
            400: openapi.Response(description="Invalid update data")
        }
    )
    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        form = LinkForm(instance=link)
        unlinked_collections = (Collection.objects.filter(user=request.user)
                                .exclude(id__in=link.collections.all().values_list('id', flat=True)))
        return render(request, 'link_form.html', {
            'form': form,
            'link': link,
            'unlinked_collections': unlinked_collections,
        })

    def post(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            link = form.save()
            selected_collections = request.POST.getlist('collections')
            link.collections.add(*selected_collections)
            return redirect('home')
        unlinked_collections = (Collection.objects.filter(user=request.user)
                                .exclude(id__in=link.collections.all().values_list('id', flat=True)))
        return render(request, 'link_form.html', {
            'form': form,
            'link': link,
            'unlinked_collections': unlinked_collections,
        })

class LinkDeleteView(View):
    @swagger_auto_schema(
        operation_description="Delete a link for the authenticated user.",
        responses={
            200: openapi.Response(description="Redirect to home page"),
            404: openapi.Response(description="Link not found")
        }
    )
    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        link.delete()
        return redirect('home')

class HomeView(View):
    @swagger_auto_schema(
        operation_description="Get the home page with links and collections for the authenticated user.",
        responses={
            200: openapi.Response(description="Home page with links and collections")
        }
    )
    def get(self, request):
        links = Link.objects.filter(user=request.user)
        collections = Collection.objects.filter(user=request.user)
        return render(request, 'home.html', {'links': links, 'collections': collections})

class PasswordChangeView(View):
    @swagger_auto_schema(
        operation_description="Change the password of the authenticated user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Old password'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='Confirm new password')
            }
        ),
        responses={
            200: openapi.Response(description="Password successfully changed"),
            400: openapi.Response(description="Invalid password change request"),
            401: openapi.Response(description="Unauthorized (wrong password or user)")
        }
    )
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'password_change.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        return render(request, 'password_change.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change_form.html'

class CollectionRemoveLinkView(View):
    @swagger_auto_schema(
        operation_description="Remove a link from a collection for the authenticated user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'collection_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Collection ID'),
                'link_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Link ID')
            }
        ),
        responses={
            200: openapi.Response(description="Link successfully removed from collection"),
            404: openapi.Response(description="Collection or link not found")
        }
    )
    def post(self, request, collection_id, link_id):
        collection = get_object_or_404(Collection, id=collection_id, user=request.user)
        link = get_object_or_404(Link, id=link_id)
        collection.links.remove(link)
        return redirect('home')