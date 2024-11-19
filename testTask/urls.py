from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),

    # Смена пароля

    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    # Сброс пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Аутентификация
    path('login/', UserLoginHTMLView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterHTMLView.as_view(), name='register'),

    # Ссылки
    path('links/', LinkListView.as_view(), name='link-list'),
    path('links/create/', LinkCreateView.as_view(), name='link-create'),
    path('links/<int:pk>/edit/', LinkUpdateView.as_view(), name='link-edit'),
    path('links/<int:pk>/delete/', LinkDeleteView.as_view(), name='link-delete'),

    # Коллекции
    path('collections/', CollectionListView.as_view(), name='collection-list'),
    path('collections/create/', CollectionCreateView.as_view(), name='collection-create'),
    path('collections/<int:pk>/edit/', CollectionUpdateView.as_view(), name='collection-edit'),
    path('collections/<int:pk>/delete/', CollectionDeleteView.as_view(), name='collection-delete'),
    path('collections/<int:collection_id>/remove-link/<int:link_id>/', CollectionRemoveLinkView.as_view(), name='collection-remove-link'),

]
