from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..forms import UserRegistrationForm, UserLoginForm


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
