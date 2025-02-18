from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import LinkViewSet, CollectionViewSet, UserViewSet, login_view
from .views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='api-user')
router.register(r'api/links', LinkViewSet, basename='api-link')
router.register(r'api/collections', CollectionViewSet, basename='api-collection')

urlpatterns = [
    # API URLs
    path('', include(router.urls)),
    path('api/login/', login_view, name='api-login'),

    # Existing URLs
    path('home', HomeView.as_view(), name='home'),

    # Смена пароля

    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    # Сброс пароля
    path('password_reset/', PasswordChangeView.as_view(), name='password_reset'),

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
    path('collections/<int:collection_id>/remove-link/<int:link_id>/', CollectionRemoveLinkView.as_view(),
         name='collection-remove-link'),
]
