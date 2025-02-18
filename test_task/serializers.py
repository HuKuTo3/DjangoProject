from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Link, Collection


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'url', 'title', 'description', 'created_at', 'user']
        read_only_fields = ['user']


class CollectionSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'created_at', 'user', 'links']
        read_only_fields = ['user']
