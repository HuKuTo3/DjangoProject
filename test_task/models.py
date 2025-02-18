from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from drf_yasg import openapi


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collections'
    )

    def __str__(self):
        return self.name


class Link(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    image = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=50, default='website')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='links'
    )
    collections = models.ManyToManyField(Collection, related_name='links', blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'url'], name='unique_user_link')
        ]

    def __str__(self):
        return self.title


link_serializer = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description="Заголовок ссылки"),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description="Описание ссылки"),
        'url': openapi.Schema(type=openapi.TYPE_STRING, description="URL ссылки"),
        'image': openapi.Schema(type=openapi.TYPE_STRING, description="URL изображения для ссылки"),
        'type': openapi.Schema(type=openapi.TYPE_STRING, description="Тип ссылки (например, 'website')"),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                     description="Дата и время создания ссылки"),
        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                     description="Дата и время последнего обновления ссылки"),
    },
)

collection_serializer = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description="Название коллекции"),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description="Описание коллекции"),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                     description="Дата и время создания коллекции"),
        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                     description="Дата и время последнего обновления коллекции"),
    },
)

custom_user_serializer = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя"),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description="Электронная почта пользователя"),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя"),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="Фамилия пользователя"),
        'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Активен ли пользователь"),
    },
)
